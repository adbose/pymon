# simple python socket server to handle multiple client devices
import socket
import os
from _thread import *
import email

server_socket = socket.socket()
host = '127.0.0.1'
port = 1233
thread_count = 0

try:
    server_socket.bind((host, port))
except socket.error as e:  # email if any connection error
    error_message  = str(e)
    print(error_message)
    email.send_alert_email(error_message)

print('Waitiing for a connection...')
server_socket.listen(5)  # can listen up to 5 devices


# callback function to exchange data between 2 connected sockets
def threaded_client(connection):
    connection.send(str.encode('PyMon is Monitoring this device'))
    while True:
        data = connection.recv(2048)
        data = data.decode('utf-8')
        print("Device Data: ", data)
        reply = 'Server received: ' + data

        if not data:
            email.send_alert_email("Server stopped receiving data")
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
