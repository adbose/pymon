# simple python socket server to handle multiple clients

import socket
import os
from _thread import *

server_socket = socket.socket()
host = '127.0.0.1'
port = 1233
thread_count = 0

try:
    server_socket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a connection...')
server_socket.listen(5)


def threaded_client(connection):
    connection.send(str.encode('PyMon is Monitoring this device'))
    while True:
        data = connection.recv(2048)
        data = data.decode('utf-8')
        print("Device Data: ", data)
        reply = 'Server received: ' + data

        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

# Server loop
while True:
    client, address = server_socket.accept()
    print('Connected to device: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (client,))  # method available from the _thread 
    thread_count += 1
    print('Thread Number: ' + str(thread_count))


server_socket.close()
