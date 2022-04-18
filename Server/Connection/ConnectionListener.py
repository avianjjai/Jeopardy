import threading
import socket
from Player import Player
from Data.Data import lock

class ConnectionListener(threading.Thread):
    def __init__(self, IP, PORT) -> None:
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.IP = IP
        self.PORT = PORT
        self.SERVER_SOCKET = None
        self.players = []

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        try:
            self.SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Server Socket Created Successfully')
        except socket.error as err:
            print('Server Socket Creation failed with error %s' %(err))

        while True:
            try:
                self.SERVER_SOCKET.bind((self.IP, self.PORT))
                print('socket binded to %s' %(self.PORT))
                break
            except:
                continue

        self.SERVER_SOCKET.listen(5)
        print('socket is listening')

        while self.stopped() == False:
            c, addr = self.SERVER_SOCKET.accept()
            print('Listen:', addr)
            player_attr = dict(
                CLIENT_IP = addr[0],
                CLIENT_PORT = addr[1],
                CLIENT_SOCKET = c,
            )

            lock.acquire()
            self.players.append(Player(**player_attr))
            lock.release()


        self.SERVER_SOCKET.close()