import tkinter as tk
import socket
from win32api import GetMonitorInfo, MonitorFromPoint
from threading import Thread
from datetime import datetime

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.title('code collab')
root.geometry(f'{screen_width}x{screen_height - 80}')
root.config(bg='gray25')
root.state('zoomed')
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


def listen_for_messages(cs):
    while True:
        try:
            message_raw = cs.recv(1024).decode("utf-8")
            print(message_raw)
        except Exception as e:
            print(e)


def on_key(event):
    pass


collab_box.bind('<Key>', on_key)

listen_thread = Thread(target=listen_for_messages, args=(client_socket,))
listen_thread.daemon = True
listen_thread.start()

while True:
    root.update_idletasks()
    root.update()
