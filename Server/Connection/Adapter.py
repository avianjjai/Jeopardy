import socket
import pickle
import threading
from turtle import clear
from Data.Data import lock

class Adapter:
    def __init__(self, CLIENT_IP, CLIENT_PORT, CLIENT_SOCKET) -> None:
        self.State = dict(
            CLIENT_IP = CLIENT_IP,
            CLIENT_PORT = CLIENT_PORT,
        )
        self.CLIENT_SOCKET = CLIENT_SOCKET
        self.listener = None

    def __del__(self):
        self.CLIENT_SOCKET.close()

    def send(self, data):
        stream = pickle.dumps(data)
        self.CLIENT_SOCKET.send(stream)

    def recv(self):
        while True:
            try:
                stream = self.CLIENT_SOCKET.recv(1024)
                data = pickle.loads(stream)
                break
            except:
                continue
        return data