'''
Common functions for recieving and sending python objects through TCP sockets
Author: Jack
'''

import json
import struct


def read_blob(sock, size):
    ''' Returns a `str` instance containing a JSON document
        from the `sock` connection (`socket` object) of expected length `size`.
        If the recieved data is shorter then `size` raises
        `Exception('Socket closed)`'''
    buf = b''
    while len(buf) != size:
        ret = sock.recv(size - len(buf))
        if not ret:
            raise Exception('Socket closed')
        buf += ret
    return buf


def read_long(sock):
    ''' Returns an `long` instance
        from the `sock` connection (`socket` object).'''
    size = struct.calcsize('i')
    data = read_blob(sock, size)
    x, = struct.unpack('i', data)
    return x


def read_object(sock):
    ''' Returns a python object
        from the `sock` connection (`socket` object).
        The packages are expected to be first first a
        package describing the lenght of the data then the serialized data'''
    datasize = read_long(sock)
    data = read_blob(sock, datasize)
    return json.loads(data.decode('utf-8'))


def send_object(obj, sock):
    '''Sends the Python object `obj` to a given
    adress `adr` through the socket object `sock`'''
    jdata = json.dumps(obj)
    sock.sendall(struct.pack('i', len(jdata)) + jdata.encode('utf-8'))
