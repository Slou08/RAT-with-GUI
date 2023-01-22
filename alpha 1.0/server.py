import socket

host = socket.gethostbyname(socket.gethostname())
port = 8081

server = socket.socket()
server.bind((host, port))

print(f'Server started at {host}:{port}')
print('Waiting for client to connect...')

server.listen(1)
client, client_address = server.accept()

print(f'{client_address} connected to server')

while True:
    command = input('Enter command: ')
    command = command.encode()
    client.send(command)
    print('Command sent to client')
    output = client.recv(1024)
    output = output.decode()
    print(f'Output from client: {output}')