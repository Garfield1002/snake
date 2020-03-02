# -*- coding: utf-8 -*-
'''
(\/)
(oO)
c(")(")
Author: Jack
'''

import curses
from curses import wrapper
import locale
import random


locale.setlocale(locale.LC_ALL, '')


class Snake():
    def __init__(self):
        # settings
        curses.curs_set(False)

        # parameters
        self.height = 21
        self.width = 50
        self.inputs = {100: (2, 0),
                       119: (0, -1),
                       115: (0, 1),
                       97: (-2, 0)}  # wasd

        # vars
        self.x = self.width // 2
        self.y = self.height // 2
        self.direction = (2, 0)
        self.body = []
        self.fruit = (0, 0)
        self.grow = False
        self.score = 0

        # creates the game window
        self.win = curses.newwin(self.height, self.width, 1, 1)

        # adds borders
        '''
        self.win.border(ord(u'\u2550'.encode('utf-8')),  # left side
                        ord(u'\u2550'.encode('utf-8')),  # right side
                        ord(u'\u2551'.encode('utf-8')),  # bottom side
                        ord(u'\u2551'.encode('utf-8')),  # top side
                        ord(u'\u2554'.encode('utf-8')),  # top left corner
                        ord(u'\u2557'.encode('utf-8')),  # top right corner
                        ord(u'\u255A'.encode('utf-8')),  # bottom left corner
                        ord(u'\u255D'.encode('utf-8')))  # bottom right corner
        '''
        self.win.border(ord('#'), ord('#'), ord('#'), ord('#'), ord('#'), ord('#'), ord('#'), ord('#'))

        self.win.addstr(self.height // 2,
                        (self.width - 23) // 2,
                        'PRESS ANY KEY TO START')

        # awaits user input
        self.win.refresh()
        self.win.getch()

        # remove begining text
        self.win.addstr(self.height // 2,
                        (self.width - 23) // 2,
                        '                      ')

        # initializes the player
        self.x, self.y = (self.width // 4) * 2, self.height // 2
        self.win.addstr(self.y, self.x, 'O')
        self.body.append((self.x, self.y))
        self.add_fruit()

    def play(self):
        self.win.timeout(100)

        # loops during the game
        while True:
            # gets the user input
            pressed = self.win.getch()

            # checks if the input is valid
            if pressed in self.inputs.keys():
                if tuple(x + y for x, y in zip(self.inputs[pressed], self.direction)) != (0, 0):
                    self.direction = self.inputs[pressed]

            # checks if the user pressed the escape key
            if pressed == 27:  # the esc key
                raise Exception('user abort')

            # moves the head
            head = tuple(x + y for x, y in zip(self.body[-1], self.direction))

            if head in self.body:
                raise Exception('collision with self')

            self.body.append(head)
            x, y = head
            if x <= 0 or x >= self.width - 1 or y <= 0 or y >= self.height - 1:
                raise Exception('collision wall')

            if head == self.fruit:
                self.score += 1
                self.win.addstr(0, 3, 'Score: {0}'.format(self.score))
                self.grow = True
                self.add_fruit()

            self.win.addstr(y, x, u'\u25CF'.encode('utf-8'))

            # moves the tail
            if not self.grow:
                x, y = self.body.pop(0)
                self.win.addstr(y, x, ' ')
            else:
                self.grow = False

            # refreshes the game window
            self.win.refresh()

    def add_fruit(self):
        available_couples = []
        for x in range(1, (self.width - 2) // 2):
            for y in range(1, self.height - 2):
                if not (x * 2, y) in self.body:
                    available_couples.append((x * 2, y))

        # adds a fruit
        x, y = random.sample(available_couples, 1).pop()
        self.fruit = (x, y)
        self.win.addstr(y, x, '$')


def main(scr):
    game = Snake()
    try:
        game.play()
    except Exception as e:
        scr.addstr(0, 0, str(e))
        scr.addstr(2, 0, 'Score: {0}'.format(game.score))
        scr.refresh()
        scr.getkey()
        pass


if __name__ == "__main__":
    wrapper(main)
