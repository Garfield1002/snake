'''
Author: Jack
'''
import socket
import socket_utils
import json
import snake
import time
import random


class SnakeServer():
    def __init__(self, max_players, ip):
        self.max_players = 2  # max_players
        self.height = 21  # TEMPORARY
        self.width = 50  # TEMPORARY
        self.snakes = []
        self.socket = socket.socket()
        self.board = None
        self.ip = ip
        # open the config.json file
        with open('config.json') as f:
            self.cfg = json.load(f)
        self.tick = self.cfg.get('server_tick')  # in milliseconds

    # awaits players
    def _lobby(self):
        print('Awaiting players')
        self.socket.bind((self.ip, self.cfg.get("port")))
        self.socket.listen(self.cfg.get("backlog"))
        self._display(['Awaiting Players'])

        # awaits connections
        while len(self.snakes) < self.max_players:
            self.handle_package('Lobby')

    # main event
    def _game(self):
        previous_tick = time.time()

        # Countdown
        down = 4
        while down > 0:
            self.handle_package('Countdown')

            if time.time() >= previous_tick + 1:
                print('Game starting in: {0}'.format(down - 1), end='\r')
                self._display(['Game starting in: {0}'.format(down - 1)])
                for snake_instance in self.snakes:
                    snake_instance.beep = 1
                previous_tick = time.time()
                down -= 1

        print('Game started                       ')
        self._display([' '])
        snake_instance.beep = 3

        self._add_fruit()
        dead = 0
        while len(self.snakes) > dead:
            # listens to socket server
            self.handle_package('Game')

            # updates the game every tick
            if time.time() >= previous_tick + self.tick * 10**(-3):
                previous_tick = time.time()

                for snake_instance in self.snakes:
                    if snake_instance.alive:
                        # moves the head
                        head = tuple(x + y
                                     for x, y in zip(snake_instance.body[-1],
                                                     snake_instance.direction))

                        for foe in self.snakes:
                            if head in foe.body:
                                snake_instance.alive = False

                        snake_instance.body.append(head)

                        x, y = head
                        collision = (x <= 0 or x >= self.width - 1 or y <= 0
                                     or y >= self.height - 1)

                        if collision:
                            snake_instance.alive = False

                        if not snake_instance.alive:
                            for x, y in snake_instance.body[:-1]:
                                self.board[x][y] = ' '
                            dead += 1
                            continue

                        if head == self.fruit:
                            snake_instance.score += 1
                            snake_instance.grow = True
                            snake_instance.beep += 1
                            self._add_fruit()

                        self.board[x][y] = snake_instance.skin

                        # moves the tail
                        if not snake_instance.grow:
                            x, y = snake_instance.body.pop(0)
                            self.board[x][y] = ' '
                        else:
                            snake_instance.grow = False

    # adds a fruit to an available spot
    def _add_fruit(self):
        available_couples = []
        for x in range(2, self.width - 2, 2):
            for y in range(1, self.height - 2):
                available_couples.append((x, y))

        for foe in self.snakes:
            if foe.alive:
                for el in foe.body:
                    available_couples.remove(el)

        x, y = random.sample(available_couples, 1).pop()
        self.board[x][y] = '$'
        self.fruit = (x, y)

    # converts a string to a table for client to display
    def _display(self, L):
        ret = []
        for i in range(self.width):
            aux = []
            for j in range(self.height):
                aux.append(' ')
            ret.append(aux)

        y = (self.height - len(L) - 1) // 2
        for i, s in enumerate(L):
            x = (self.width - len(s)) // 2
            for j, c in enumerate(s):
                ret[x + j - 1][y + i - 1] = c
        self.board = ret

    # handles incoming packages
    def handle_package(self, event):
        connection, addr = self.socket.accept()
        (s, obj) = socket_utils.read_object(connection)

        # client requesting to join a game
        if s == 'Request' and event == 'Lobby':
            print('Adding a new player to the game')
            # gets first available player id
            player_id = len(self.snakes)

            # creates a new snake instance for the player
            new_snake = snake.Snake(player_id)
            new_snake.body.append((2 * player_id + 2, 2 * player_id + 2))

            if player_id == 1:
                new_snake.skin = '@'

            # adds a snake for the new player
            self.snakes.append(new_snake)
            print('Current amount of players: {0}'.format(len(self.snakes)))
            socket_utils.send_object((player_id, self.height, self.width),
                                     connection)

        # client expecting update
        elif s == 'Update':
            socket_utils.send_object(self.board, connection)

        elif s == 'Direction':
            player_id, new_direction = obj
            self.snakes[player_id].direction = new_direction
            socket_utils.send_object((self.snakes[player_id].beep,
                                      self.snakes[player_id].alive,
                                      self.snakes[player_id].score,
                                      self.board), connection)
            if self.snakes[player_id].beep > 0:
                self.snakes[player_id].beep -= 1

        connection.close()

    def start(self):
        self._lobby()
        self._game()
