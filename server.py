import socket
from threading import Thread
from datetime import datetime

HOST = '127.0.0.1'
PORT = 42069

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

clients = []


def get_date_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def receive_message(cs, ca):
    while True:
        try:
            message = cs.recv(1024).decode()
            if not message:
                raise Exception('')

        except:
            print(f'[{get_date_now()}] Lost connection with {ca[0]}:{ca[1]}')
            clients.remove(cs)
            break

        for client in clients:
            client.send(message.encode('utf-8'))

print(f"[{get_date_now()}] Server opened on {HOST}:{PORT}")

while True:
    cs, ca = s.accept()
    clients.append(cs)

    print(f"[{get_date_now()}] Connected with {ca[0]}:{ca[1]}")
    client_thread = Thread(target=receive_message, args=(cs, ca))
    client_thread.daemon = True
    client_thread.start()
