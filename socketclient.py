# Client Side
'''
(\/)
(oO)
c(")(")
Author: Jack
'''
import socket


class SocketClient():

    def __init__(self, host, host_port_number, my_port):
        self.s = socket.socket()

        # get local machine name
        self.host = host
        self.port = host_port_number

    def connect(self):
        # attempts to connect to the server
        return self.s.connect_ex(address=(self.host, self.port))

    def close(self):
        # shutsdown the connection
        self.s.close()
