import threading
from unicodedata import name
from Connection.Adapter import Adapter
from Data.Data import lock

class Player:
    def __init__(self, CLIENT_IP, CLIENT_PORT, CLIENT_SOCKET) -> None:
        self.State = dict(
            name = "",
            active = False,
            score = 0,
            id = -1,
        )

        adapter_attr = dict(
            CLIENT_IP = CLIENT_IP,
            CLIENT_PORT = CLIENT_PORT,
            CLIENT_SOCKET = CLIENT_SOCKET,
        )
        self.adapter = Adapter(**adapter_attr)


    def run(self, command):
        if command == 'HAND_SHAKE':
            pck = self.adapter.recv()
            self.executePck(pck)
    
    def stop(self):
        self._stop.set()

    def setState(self, keyValue):
        for key, value in keyValue.items():
            self.State[key] = value
        
        self.updateState()

    def updateState(self):
        pass

    def executePck(self, pck):
        if pck['type'] == 'HAND_SHAKE':
            self.setState(dict(
                name = pck['name'],
                active = True,
            ))


        elif pck['type'] == '':
            pass


    def start(self):
        print("Adapter Connected")
        