# client file of remote administration tool

import socket
import sys
import os
import time
import threading
import subprocess
import platform
import getpass
import shutil

host = socket.gethostbyname(socket.gethostname())

# set up socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 12345))

# wait for command from server
while True:
    cmd = s.recv(1024).decode()
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
        filename = s.recv(1024).decode()
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                data = f.read(1024)
                while data:
                    s.send(data)
                    data = f.read(1024)
            print('File sent')
        else:
            s.send('File not found'.encode())
    elif cmd == 'put':
        # put file on client
        filename = s.recv(1024).decode()
        data = s.recv(1024)
        with open(filename, 'wb') as f:
            while data:
                f.write(data)
                data = s.recv(1024)
        print('File received')
    else:
        # execute command
        output = subprocess.getoutput(cmd)
        if not output:
            output = 'Command executed'
        s.send(output.encode())
    
# close socket
s.close()
