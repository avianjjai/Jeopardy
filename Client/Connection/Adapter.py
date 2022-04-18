import socket
import pickle
from Data.Data import lock

class Adapter:
    def __init__(self, SERVER_IP, SERVER_PORT) -> None:
        self.State = dict(
            SERVER_IP = SERVER_IP,
            SERVER_PORT = SERVER_PORT,
            status = 'RUNNING'
        )
        self.SERVER_SOCKET = self.connect()
        print('Connection Successful')

    def __del__(self):
        self.SERVER_SOCKET.close()
        print('Adapter Closed')

    def setState(self, keyValue):
        for key, value in keyValue.items():
            self.State[key] = value

    def connect(self):
        SERVER_SOCKET = socket.socket()
        while True:
            try:
                SERVER_SOCKET.connect((self.State['SERVER_IP'], self.State['SERVER_PORT']))
                break
            except:
                continue
        return SERVER_SOCKET

    def close(self):
        self.SERVER_SOCKET.close()

    def send(self, data):
        stream = pickle.dumps(data)
        self.SERVER_SOCKET.send(stream)

    def recv(self):
        while self.State['status'] != 'OVER':
            try:
                stream = self.SERVER_SOCKET.recv(1024)
                data = pickle.loads(stream)
                break
            except:
                if self.State['status'] == 'OVER':
                    data = None
                    break
                else:
                    continue

        return data