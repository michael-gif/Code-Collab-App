import tkinter as tk
import socket
from win32api import GetMonitorInfo, MonitorFromPoint
from threading import Thread
from datetime import datetime

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.title('code collab')
root.geometry(f'{500}x{250 - 80}')
root.config(bg='gray25')
#root.state('zoomed')
root.update()

monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")
taskbar_height = monitor_area[3] - work_area[3]

collab_box = tk.Text(root, bg='black', fg='white')
collab_box.place(x=10, y=10, width=root.winfo_width() - 20, height=root.winfo_height() - 20)

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 42069

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

message_queue = []

def listen_for_messages(cs):
    while True:
        message_raw = cs.recv(1024).decode("utf-8")
        parts = message_raw.split('\n')
        line_number = parts[1]
        line = parts[0]
        message_queue.append((line_number, line))


def on_key(event):
    cursor = collab_box.index(tk.INSERT)
    line_number = cursor.split('.')[0]
    text = collab_box.get('1.0', tk.END)
    lines = text.split('\n')
    current_line = lines[int(line_number) - 1]
    #print([current_line,cursor])
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
            line_number = message[0]
            replacement_line = message[1]
            lines = collab_box.get('1.0', tk.END).split('\n')
            new_line_number = int(line_number) - 1
            if int(line_number) <= len(lines):
                old_line = lines[new_line_number]
                if old_line != replacement_line:
                    collab_box.delete(line_number + '.0', str(int(line_number) + 1) + '.0')
                    collab_box.insert(line_number + '.0', replacement_line)
            else:
                #collab_box.insert(tk.END, '\n')
                collab_box.insert(line_number + '.0', replacement_line)
        message_queue.clear()
