import curses
import locale

class Game_screen():
    def __init__(border=True):
        pass


def draw_borders(win, min_x, min_y, max_x, max_y):
    locale.setlocale(locale.LC_ALL, "")

    # corners
    win.addstr(min_y, min_x, u'\u2554'.encode('utf-8'))
    win.addstr(min_y, max_x, u'\u2557'.encode('utf-8'))
    win.addstr(max_y, min_x, u'\u255A'.encode('utf-8'))
    win.addstr(max_y, max_x, u'\u255D'.encode('utf-8'))

    # lines
    for i in range(min_x + 1, max_x):
        win.addstr(min_y, i, u'\u2550'.encode('utf-8'))
        win.addstr(max_y, i, u'\u2550'.encode('utf-8'))
    for i in range(min_y + 1, max_y):
        win.addstr(i, min_x, u'\u2551'.encode('utf-8'))
        win.addstr(i, max_x, u'\u2551'.encode('utf-8'))
