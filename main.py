import tkinter as tk
import socket
from tkinter import ttk
from win32api import GetMonitorInfo, MonitorFromPoint
from threading import Thread

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.title('code collab')
#root.geometry(f'{500}x{250 - 80}')
root.config(bg='gray25')
root.state('zoomed')
root.update()

monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")
taskbar_height = monitor_area[3] - work_area[3]

tabControl = ttk.Notebook(root)
code_collab_tab = ttk.Frame(tabControl)
code_collab_tab.update()

tabControl.add(code_collab_tab, text='Code Collab')
tabControl.place(x=10, y=10, width=root.winfo_width() - 20, height=root.winfo_height() - 20)
tabControl.update()

text_box = tk.Text(code_collab_tab, bg='black', fg='white', insertbackground='white')
text_box.place(x=0, y=0, width=tabControl.winfo_width(), height=tabControl.winfo_height())

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 42069

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

message_queue = []


def listen_for_messages(cs):
    while True:
        message_raw = cs.recv(1024).decode("utf-8")
        parts = message_raw.split('\n')
        message_queue.append(parts)


def on_key(event):
    cursor = text_box.index(tk.INSERT)
    line_number = cursor.split('.')[0]
    lines = text_box.get('1.0', tk.END).split('\n')
    current_line = lines[int(line_number) - 1]
    client_socket.send((current_line + "\n" + line_number).encode('utf-8'))


root.bind('<Key>', on_key)

listen_thread = Thread(target=listen_for_messages, args=(client_socket,))
listen_thread.daemon = True
listen_thread.start()

while True:
    root.update_idletasks()
    root.update()
    if message_queue:
        for message in message_queue:
            replacement_line = message[0]
            line_number = message[1]
            lines = text_box.get('1.0', tk.END).split('\n')
            if lines[-1] == '':
                lines.pop(-1)
            line_index = int(line_number) - 1
            if line_index + 1 <= len(lines):
                old_line = lines[line_index]
                if old_line != replacement_line:
                    text_box.replace(line_number + '.0', line_number + '.' + str(len(old_line)), replacement_line)
            else:
                text_box.insert(str(line_index + 2) + '.0', replacement_line + '\n')
            text_box.see(tk.END)
        message_queue.clear()
