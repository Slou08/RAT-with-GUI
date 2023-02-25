# the same as alpha 1.4, but with a gui for the server
import tkinter as tk
import socket
import threading
import time
import sys
import os

def handle_connection(client: socket.socket, addr):
    print(f'Client connected: {addr}')

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 1234))
    s.listen(1)
    
    while True:
        client, addr = s.accept()
        threading.Thread(target=handle_connection, args=(client, addr)).start()