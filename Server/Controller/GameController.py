from Data.ServerData import SERVER_IDENTITY
from Connection.ConnectionListener import ConnectionListener
from Data.Data import lock
from Controller.Game import Game
import threading

class GameController(threading.Thread):
    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.State = dict(
            active_games = [],
            active_count = 0,
            inactive_games = [],
            inactive_count = 0,
            _stop = threading.Event()
        )

    def stop(self):
        self.State['_stop'].set()

    def stopped(self):
        return self.State['_stop'].isSet()

    def run(self):
        print('GameController Started')
        listener_attr = dict(
            IP = SERVER_IDENTITY['IP'],
            PORT = SERVER_IDENTITY['PORT']
        )
        connectionlistener = ConnectionListener(**listener_attr)
        connectionlistener.start()

        while self.stopped() == False:
            self.updateState()
            if connectionlistener.players:
                lock.acquire()
                player = connectionlistener.players.pop(0)
                lock.release()

                threading.Thread(target=player.run, args=('HAND_SHAKE', )).start()
                self.addPlayer(player)

    
    def addPlayer(self, player):
        ADD_SUCCESSFUL = False
        
        for i in range(self.State['inactive_count']):
            game = self.State['inactive_games'][i]
            if game.spaceAvailable():
                game.addPlayer(player)
                ADD_SUCCESSFUL = True

        if ADD_SUCCESSFUL == False:
            game = Game(3)
            game.addPlayer(player)
            self.State['inactive_games'].append(game)
            self.State['inactive_count'] += 1
            ADD_SUCCESSFUL = True

        self.updateState()
            

    def setState():
        pass

    def delete_complete_games(self):
        i = 0
        while i<self.State['active_count']:
            game = self.State['active_games'][i]
            if game.State['gameMode'] == 'OVER':
                temp = self.State['active_games'].pop(i)
                self.State['active_count'] -= 1
                temp.stop()
            else:
                i += 1


    def switch_inactive_to_active_list(self):
        i = 0
        while i<self.State['inactive_count']:
            game = self.State['inactive_games'][i]
            if len(game.State['players']) == game.State['allowed_players']:
                game = self.State['inactive_games'].pop(i)
                self.State['inactive_count'] -= 1

                self.State['active_games'].append(game)
                self.State['active_count'] += 1
                game.start()
            else:
                i += 1

    def updateState(self):
        self.delete_complete_games()
        self.switch_inactive_to_active_list()
