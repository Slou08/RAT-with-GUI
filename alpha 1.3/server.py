import socket
import threading

def handle_client(client_socket: socket.socket, client_addr):
    print(f'Client connected: {client_addr}')
    try:
        while True:
            msg = client_socket.recv(1024).decode()
            client_socket.send(f'Du hast "{msg}" gesendet"'.encode())
    except:
        print('Connection closed')
    finally:
        client_socket.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1234))
s.listen(1)

while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()