import threading
from Data.ServerData import SERVER_IDENTITY
from Connection.Adapter import Adapter
from View.GameUI import GameUI
from Data.Data import lock
from tkinter import Tk
from View.QuestionUI import QuestionUI
import time

class GameController:
    def __init__(self) -> None:
        print('GameController Started')

        adapter_attr = dict(
            SERVER_IP = SERVER_IDENTITY['IP'],
            SERVER_PORT = SERVER_IDENTITY['PORT']
        )
        self.adapter = Adapter(**adapter_attr)

        pak = dict(
            type = 'HAND_SHAKE',
            name = input('Enter Name: '),
        )
        self.adapter.send(pak)

        pck = self.adapter.recv()
        self.executePck(pck)

        self.game = None
        self.UI_thread = None
        self.sendBuffer = []
        self.questionWindow = None
        self.questionRoot = None
        self.question_thread = None
        self.answer = []
        self.gameStatus = 'RUNNING'

    def startUI(self, pck):
        root = Tk()
        root.resizable(width=False, height=False)
        attr = dict(
            master = root,
            width = 1000,
            height = 800,
            bg = '#B49D98',
            players_count = pck['players_count'],
            players = pck['players'],
            id = pck['id'],
            categories = pck['categories'],
            scoresPerCategory = pck['scoresPerCategory'],
            category_columns = pck['category_columns'],
            sendBuffer = self.sendBuffer
        )
        self.game = GameUI(**attr)
        root.mainloop()
        self.gameStatus = 'OVER'
        self.adapter.setState(dict(
            status = 'OVER'
        ))

        del self.adapter
        print('StartUI Thread Closed')

    def executePck(self, pck):
        if pck['type'] == 'HAND_SHAKE':
            self.UI_thread = threading.Thread(target=self.startUI, args=(pck, ))
            self.UI_thread.start()
            
        if pck['type'] == 'FIN':
            self.game.destroy()

        elif pck['type'] == 'PAY_LOAD':
            while not self.game:
                continue
            self.game.setVisit(pck['visit'])
            self.game.setPlayer(pck['players'])
            self.game.setState(dict(
                turn = pck['turn'],
                active = self.game.State['id'] == pck['turn'],
                submit_button_state = 'disabled',
                exit_button_state = 'disabled',
            ))

            self.game.questionAnswer.setState(dict(
                question = '',
                answer = '',
                question_window_state = 'disabled',
            ))
        
        elif pck['type'] == 'QUESTION':
            self.game.setVisit(pck['visit'])
            self.game.setPlayer(pck['players'])
            self.game.setState(dict(
                turn = pck['turn'],
                active = False,
            ))

            self.game.State['questionAnswer']['row'] = pck['row']
            self.game.State['questionAnswer']['col'] = pck['col']

            if self.game.State['id'] == pck['turn']:
                self.game.setState(dict(
                    submit_button_state = 'active',
                    exit_button_state = 'active',
                ))
                self.game.questionAnswer.setState(dict(
                    question = pck['question'],
                    answer = '',
                    question_window_state = 'normal',
                ))

            else:
                self.game.setState(dict(
                    submit_button_state = 'disabled',
                    exit_button_state = 'disabled',
                ))
                self.game.questionAnswer.setState(dict(
                    question = pck['question'],
                    answer = '',
                    question_window_state = 'disabled',
                ))



    def start(self):
        while self.gameStatus != 'OVER':
            try:
                pck = self.adapter.recv()
                self.executePck(pck)
            except:
                break

            if self.game.State['id'] == self.game.State['turn']:
                while not self.sendBuffer:
                    if self.gameStatus == 'OVER':
                        break
                    time.sleep(0.1)

                lock.acquire()
                pck = self.sendBuffer.pop(0)
                lock.release()

                self.adapter.send(pck)

        print('gameController.py Closed')