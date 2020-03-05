'''
Author: Jack'''
import curses
import json
import socket_utils
import socket
import time


class SnakeClient():
    def __init__(self, ip):
        self.id = None
        self.height = None
        self.width = None
        self.board = None
        self.alive = True
        self.win = None
        self.score = 0
        self.direction = (2, 0)
        self.host = ip  # '192.168.43.58'
        # open the config.json file
        with open('config.json') as f:
            self.cfg = json.load(f)
        self.port = self.cfg.get("port")
        self.tick = self.cfg.get("client_tick")
        self.inputs = self.cfg.get("inputs")
        self.default = {
            "UP": [0, 1],
            "DOWN": [0, -1],
            "LEFT": [-2, 0],
            "RIGHT": [2, 0]
            }
        self.beep = self.cfg.get("sound")
        self. art = \
            [
                ' .d8888b.                    888',
                'd88P  Y88b                   888',
                'Y88b.                        888',
                ' "Y888b.   88888b.   8888b.  888  888  .d88b.',
                '    "Y88b. 888 "88b     "88b 888 .88P d8P  Y8b',
                '      "888 888  888 .d888888 888888K  88888888',
                'Y88b  d88P 888  888 888  888 888 "88b Y8b.',
                ' "Y8888P"  888  888 "Y888888 888  888  "Y8888'
            ]

    # function to read keys
    def read_key(self):
        ch = self.win.getch()
        if ch == (27 and 91 and 65):
            return "UP"
        elif ch == (27 and 91 and 66):
            return "DOWN"
        elif ch == (27 and 91 and 67):
            return "RIGHT"
        elif ch == (27 and 91 and 68):
            return "LEFT"
        return ch

    def __main(self, scr):
        # turns off the cursor
        curses.curs_set(False)

        # gets board dimensions and id
        self.id, self.height, self.width = self.__request_join()

        # creates the game window
        self.win = curses.newwin(self.height, self.width, 1, 1)

        # adds a border
        self.win.border(ord('#'),
                        ord('#'),
                        ord('#'),
                        ord('#'),
                        ord('#'),
                        ord('#'),
                        ord('#'),
                        ord('#'))
        for i, l in enumerate(self.art):
            self.win.addstr(2+i, 2, l)

        while True:
            # gets user input
            self.win.timeout(self.tick)

            # gets the time the client started waiting
            start_time = time.time()

            # gets the command of the user, waiting a maximum
            # of client_tick time
            pressed = self.read_key()

            # gets the remaining amount of time that needs to be waited
            remaining_wait = self.tick * 10 ** (-3) \
                - (time.time() - start_time)

            if remaining_wait > 0:
                time.sleep(remaining_wait)

            # checks if the input is valid
            # json keys are all strings
            if str(pressed) in self.inputs.keys():
                if tuple(x + y for x, y in
                         zip(tuple(self.inputs[str(pressed)]),
                             self.direction)) != (0, 0):
                    self.direction = tuple(self.inputs[str(pressed)])

            # are the arrow keys being used
            elif pressed in self.default.keys():
                if tuple(x + y for x, y in
                         zip(tuple(self.default[pressed]),
                             self.direction)) != (0, 0):
                    self.direction = tuple(self.default[pressed])

            # checks if the user pressed the escape key
            elif pressed == self.cfg.get("escape"):  # the esc key
                raise Exception('user abort')

            # gets the board
            beep, self.alive, self.score, self.board =  \
                self.__send_direction()

            # if the player is dead quits the game
            if not self.alive:
                break

            if beep and self.beep:
                curses.beep()

            # updates the screen
            for x in range(1, self.width - 1):
                for y in range(1, self.height - 1):
                    self.win.addstr(y, x, str(self.board[x][y]))

            # prints the score
            self.win.addstr(0, 3, 'Score: {0}'.format(self.score))

            # prints the player_id
            self.win.addstr(self.height - 1, 3, 'Playeri ID: {0}'.
                                                format(self.id))

            # updates the console
            self.win.refresh()

    def safe_main(self):
        curses.wrapper(self.__main)

    def __request_join(self):
        sock = socket.socket()
        sock.connect((self.host, self.port))
        socket_utils.send_object(('Request', 0), sock)
        return socket_utils.read_object(sock)

    def __send_direction(self):
        sock = socket.socket()
        sock.connect((self.host, self.port))
        socket_utils.send_object(
            ('Direction', (self.id, self.direction)), sock)
        return socket_utils.read_object(sock)
