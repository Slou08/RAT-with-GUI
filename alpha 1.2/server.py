# remote adminstration tool server

import socket
import sys
import os
import time
import threading

host = socket.gethostbyname(socket.gethostname())
port = 9999

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)

# wait for connection
print('Waiting for connection...')
conn, addr = s.accept()

# wait for command input and send to client
while True:
    cmd = input('Enter command: ')
    conn.send(cmd.encode())
    if cmd == 'exit':
        break
    elif cmd == 'help':
        print('''
        Commands:
        help - display this message
        exit - exit the program
        get - get a file from the client
        put - put a file on the client
        ''')
    elif cmd == 'get':
        # get file from client
        filename = input('Enter file name: ')
        conn.send(filename.encode())
        data = conn.recv(1024)
        if data.decode() == 'File not found':
            print('File not found')
        else:
            with open(filename, 'wb') as f:
                while data:
                    f.write(data)
                    data = conn.recv(1024)
            print('File received')
    elif cmd == 'put':
        # put file on client
        filename = input('Enter file name: ')
        if os.path.isfile(filename):
            conn.send(filename.encode())
            with open(filename, 'rb') as f:
                data = f.read(1024)
                while data:
                    conn.send(data)
                    data = f.read(1024)
            print('File sent')
        else:
            print('File not found')
    else:
        # receive output from client
        data = conn.recv(1024)
        print(data.decode())
    
# close connection
conn.close()