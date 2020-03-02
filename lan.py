import socket

sock = socket.socket()
host = socket.gethostname()
port = 12345
# print('starting up server on {0} port {1}'.format(server_adress))
sock.bind(server_adress)
sock.listen(1)
while True:
    # find connections
    connection, client_adress = sock.accept()
    try:
        data = connection.recv(999)
        print(data)
    except:
        connection.close() 
