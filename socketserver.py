'''
(\/)
(oO)
c(")(")
Author: Jack
'''
import socket


class SocketServer():
    def __init__(self, port_number, backlog=5):
        self.port = port_number
        self.s = socket.socket()
        self.host = socket.gethostname()
        self.backlog = backlog
        self.known = []

    # starts the server
    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(self.backlog)

    # accepts a connection
    def accept(self):
        return self.s.accept()  # -> socket obj, adress
