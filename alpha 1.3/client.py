import socket

client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_s.connect(('127.0.0.1', 1234))

while True:
    msg = input('Message: ')
    client_s.send(msg.encode())
    answer = client_s.recv(1024).decode()
    print(answer)