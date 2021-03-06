import curses
import snakeclient
import snakeserver
import json
import socket

width = 50
height = 21


# function to read keys
def read_key(win):
    ch = win.getch()
    if ch == (27 and 91 and 65):
        return "UP"
    elif ch == (27 and 91 and 66):
        return "DOWN"
    elif ch == (27 and 91 and 67):
        return "RIGHT"
    elif ch == (27 and 91 and 68):
        return "LEFT"
    return ch


def get_input(scr, l1, l2, prompt, expected):
    curses.curs_set(True)

    win = curses.newwin(height, width, 1, 1)
    win.border(ord('#'),
               ord('#'),
               ord('#'),
               ord('#'),
               ord('#'),
               ord('#'),
               ord('#'),
               ord('#'))
    win.addstr(height // 2 - 1,
               (width - len(l1)) // 2,
               l1)
    win.addstr(height // 2,
               (width - len(l2)) // 2,
               l2)
    curses.echo(True)
    win.addstr(height // 2 + 1,
               (width - len(prompt) - expected) // 2,
               prompt)

    return win.getstr()


def __main(scr, L):
    # creates a window
    win = curses.newwin(height, width, 1, 1)

    # adds a border
    win.border(ord('#'),
               ord('#'),
               ord('#'),
               ord('#'),
               ord('#'),
               ord('#'),
               ord('#'),
               ord('#'))

    return menu(win, L)


def warning(messages, fun, *args):
    def aux(scr, messages, fun):
        win = curses.newwin(height, width, 1, 1)
        win.border(ord('#'),
                   ord('#'),
                   ord('#'),
                   ord('#'),
                   ord('#'),
                   ord('#'),
                   ord('#'),
                   ord('#'))
        curses.curs_set(False)

        win.addstr(1,
                   1,
                   'Press "Esc" to return to main menu')
        for i, message in enumerate(messages):
            win.addstr((height - len(messages)) // 2 + i,
                       (width - len(message)) // 2,
                       message)

        while True:
            pressed = win.getch()
            if pressed == 10:  # curses.KEY_ENTER:
                return fun
            elif pressed == 27:
                return main_menu
    foo = curses.wrapper(aux, messages, fun)
    foo(*args)


def menu(win, L):
    global default_ip
    default_ip = socket.gethostbyname(socket.gethostname())
    curses.curs_set(False)

    # default attributes
    default_attr = curses.A_BOLD

    # highlight attributes
    highlight_attr = curses.A_REVERSE

    # gets the window lenght and height
    maxy, maxx = win.getmaxyx()
    miny, minx = win.getbegyx()
    height = maxy - miny
    width = maxx - minx

    # vertical padding for placing the menues
    vertical_padding = height // (len(L) + 1)

    # horizontal padding for placing the menues
    horizontal_padding = max(len(name) for name, _ in L) + 2

    selected = 0

    win.addstr(height, 1, "IP: {0}".format(default_ip))

    def update_screen():
        for i, (name, _) in enumerate(L):
            if i == selected:
                a = highlight_attr
            else:
                a = default_attr

            win.addstr((i+1) * vertical_padding, width - horizontal_padding,
                       name, a)
        win.refresh()

    update_screen()
    global cfg
    while True:
        pressed = read_key(win)

        if pressed == 10:  # curses.KEY_ENTER:
            a, fun = L[selected]
            return fun

        win.addstr(1, 1, str(pressed))

        if pressed == "UP" or pressed == cfg["keys"]["up"]:
            selected -= 1
        elif pressed == "DOWN" or pressed == cfg["keys"]["down"]:
            selected += 1
#        elif pressed == 27:  # curses.KEY_ESC
#            return lambda *args: print('See ya soon')

        selected = selected % len(L)
        update_screen()


def __join():
    ip = curses.wrapper(get_input,
                        'Enter the IP address you want to connect to.',
                        '("local" for local game)',
                        'IP: ',
                        9
                        ).decode('utf-8')

    global default_ip
    if ip == 'local' or ip == '':
        ip = default_ip

    return warning(['Press Enter to connect to', str(ip)],
                   lambda ip: snakeclient.SnakeClient(ip).safe_main(),
                   ip)


def user_input(message, tp=None):
    def aux(scr, message):
        curses.curs_set(True)
        win = curses.newwin(height, width, 1, 1)
        win.border(ord('#'),
                   ord('#'),
                   ord('#'),
                   ord('#'),
                   ord('#'),
                   ord('#'),
                   ord('#'),
                   ord('#'))
        win.addstr(height // 2 - 1,
                   (width - len(message)) // 2,
                   message)
        win.move(height // 2, width // 2)
        curses.echo(True)
        win.refresh()
        return win.getstr().decode('utf-8')
    return curses.wrapper(aux, message)


def modify_cfg():
    global cfg
    with open('config.json', 'w') as cfg_file:
        json.dump(cfg, cfg_file)


def __change_key(direction, name):
    global cfg
    for k, v in cfg["inputs"].items():
        if v == direction:
            cfg["inputs"].pop(k)
            break
    key = user_input('Press the new {0} key:'.format(name))
    cfg["inputs"][ord(key)] = direction
    cfg["keys"][name] = ord(key)
    modify_cfg()
    return __settings()


def __change_bool(name):
    global cfg
    cfg[name] = int(not cfg[name])
    modify_cfg
    return __settings()


def __host():
    ip = curses.wrapper(get_input,
                        'Enter the IP address you want to host on.',
                        '("local" for local game)',
                        'IP: ',
                        9
                        ).decode('utf-8')

    players = int(curses.wrapper(get_input,
                                 '',
                                 'Enter the amount of players.',
                                 'Max players: ',
                                 9
                                 ).decode('utf-8'))

    global default_ip
    if ip == 'local' or ip == '':
        ip = default_ip

    return warning(['Press Enter to host on', str(ip)],
                   # UNIMPLEMENTED ----------------
                   lambda ip: snakeserver.SnakeServer(players, ip).start(),
                   ip)


def __settings():
    global cfg
    settings_menu_L = [('Up Key: {0}'.format(chr(cfg["keys"]['up'])),
                        lambda *args: __change_key([0, -1], "up")),
                       ('Down Key: {0}'.format(chr(cfg["keys"]['down'])),
                        lambda *args: __change_key([0, 1], "down")),
                       ('Left Key: {0}'.format(chr(cfg["keys"]['left'])),
                        lambda *args: __change_key([-2, 0], "left")),
                       ('Right Key: {0}'.format(chr(cfg["keys"]['right'])),
                        lambda *args: __change_key([2, 0], "right")),
                       ('Sound: {0}'.format(bool(cfg["sound"])),
                        lambda *args: __change_bool("sound")),
                       ('Main Menu', main_menu)]
    fun = curses.wrapper(__main, settings_menu_L)
    return fun()


def main_menu():
    main_menu_L = [('Join', __join),
                   ('Host', __host),
                   ('Settings', __settings),
                   ('Quit', lambda *args: print('See ya soon'))]
    fun = curses.wrapper(__main, main_menu_L)
    return fun()


if __name__ == '__main__':
    global cfg
    # open the config.json file
    with open('config.json') as f:
        cfg = json.load(f)
    main_menu()
