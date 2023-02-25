# the same as alpha 1.4, but with a gui for the server
import customtkinter as ctk
import socket
import threading
import time
import sys
import os

def gui(client: socket.socket, addr):
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    
    root = ctk.CTk()
    root.title(f'Client: {addr}')
    root.geometry('900x450')
    root.resizable(False, False)
    
    
    
    
    root.mainloop()

def handle_connection(client: socket.socket, addr):
    print(f'Client connected: {addr}')
    try:
        gui(client=client, addr=addr)
    except:
        print(f'Client disconnected: {addr}')
    finally:
        client.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 1234))
    s.listen(1)
    print('Waiting for connections...')
    
    while True:
        client, addr = s.accept()
        threading.Thread(target=handle_connection, args=(client, addr)).start()

if __name__ == '__main__':
    main()