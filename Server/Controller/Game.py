import time
from Data.Data import election_database_attribute
from PersistentStorage import PersistentStorage
from Data.Data import lock
import threading
from Model.Board import Board
from Questions import election_questions, technology_questions, sports_questions

class Game(threading.Thread):
    def __init__(self, allowed_players) -> None:
        threading.Thread.__init__(self)
        
        board_attr = dict(
            categories = 3,
            scoresPerCategory = 5,
            category_columns = ['Election', 'Sports', 'Technology'],
            questions = [election_questions, sports_questions, technology_questions],
        )
        
        self.State = dict(
            allowed_players = allowed_players,
            gameMode = 'NOT_STARTED',
            players = [],
            turn = -1,
            round = 1,
            wrong_ans = 0,
            _stop = threading.Event(),
        )
        self.board = Board(**board_attr)
        self.electionDatabase = PersistentStorage(**election_database_attribute)

    def stop(self):
        self.State['_stop'].set()

    def stopped(self):
        return self.State['_stop'].isSet()

    def setState(self, keyValue):
        for key, value in keyValue.items():
            self.State[key] = value
        
        self.updateState()

    def updateState(self):
        pass

    def getWinners(self):
        players = [dict(
            id = i,
            name = self.State['players'][i].State['name'],
            score = self.State['players'][i].State['score'],
        ) for i in range(self.State['allowed_players'])],

        maxScore = float('-inf')
        for p in players:
            if p['score'] > maxScore:
                maxScore = p['score']

        winners = []
        for p in players:
            if p['score'] == maxScore:
                winners.append(p)
        return winners


    def checkAns(self, query, ansColumn, userAns):
        try:
            ans = self.electionDatabase.executeQuery(**query)
            ans = ans.getTable()[ansColumn]
            return ans.shape == (1, ) and ans[0] == userAns

        except:
            return False

    def __nextTurn(self):
        return ((self.State['turn']+1))%self.State['allowed_players']

    def spaceAvailable(self):
        return len(self.State['players']) < self.State['allowed_players']

    def addPlayer(self, player):
        player.setState(dict(
            id = len(self.State['players'])
        ))
        self.State['players'].append(player)

    def waitForAllPlayers(self):
        while True:
            active = True
            for player in self.State['players']:
                if player.State['active'] == False:
                    active = False
                    break
            
            if active:
                return

    def broadCastWithId(self, pck):
        for player in self.State['players']:
            pck_copy = {}
            for key, val in pck.items():
                pck_copy[key] = val

            pck_copy['id'] = player.State['id']
            lock.acquire()
            player.adapter.send(pck_copy)
            lock.release()

    def broadCast(self, pck):
        for player in self.State['players']:
            lock.acquire()
            player.adapter.send(pck)
            lock.release()

    def executePck(self, pck):
        if pck['type'] == 'FIN':
            send_pck = dict(
                type = 'FIN',
            )

            self.broadCast(send_pck)
            self.setState(dict(
                gameMode = 'OVER',
            ))
        
        
        elif pck['type'] == 'PAY_LOAD':
            self.setState(dict(
                gameMode = 'RUNNING',
                turn = self.__nextTurn(),
                wrong_ans = 0,
            ))

            self.board.setVisit(pck['visit'])

            send_pck = dict(
                type = 'PAY_LOAD',
                turn = self.State['turn'],
                visit = self.board.getVisit(),
                players = [dict(
                    name = self.State['players'][i].State['name'],
                    score = self.State['players'][i].State['score'],
                ) for i in range(self.State['allowed_players'])],
            )

            self.broadCast(send_pck)

        elif pck['type'] == 'REQUEST_QUESTION':
            self.board.setVisit(pck['visit'])

            send_pck = dict(
                type = 'QUESTION',
                turn = self.State['turn'],
                row = pck['row'],
                col = pck['col'],
                question = self.board.State['questions'][pck['row']][pck['col']]['question'],
                visit = self.board.getVisit(),
                players = [dict(
                    name = self.State['players'][i].State['name'],
                    score = self.State['players'][i].State['score'],
                ) for i in range(self.State['allowed_players'])],
            )
            self.broadCast(send_pck)

        elif pck['type'] == 'ANSWER':
            self.board.setVisit(pck['visit'])

            question = self.board.State['questions'][pck['row']][pck['col']]
            attr = dict(
                query = question['query'],
                ansColumn = question['ansColumn'],
                userAns = pck['answer'],
            )

            player = self.State['players'][self.State['turn']]
            self.setState(dict(
                gameMode = 'RUNNING',
                turn = self.__nextTurn(),
            ))

            # if answer is correct or all gives wrong answers
            if self.checkAns(**attr) or self.State['wrong_ans']+1 == self.State['allowed_players']:
                gain = -1 if self.State['wrong_ans']+1 == self.State['allowed_players'] else 1

                player.setState(dict(
                    score = player.State['score'] + gain*self.board.State['cells'][pck['row']][pck['col']].State['value'],
                ))

                self.setState(dict(
                    wrong_ans = 0,
                ))

                send_pck = dict(
                    type = 'PAY_LOAD',
                    turn = self.State['turn'],
                    visit = self.board.getVisit(),
                    players = [dict(
                        name = self.State['players'][i].State['name'],
                        score = self.State['players'][i].State['score'],
                    ) for i in range(self.State['allowed_players'])],
                )
                self.broadCast(send_pck)

            # if answer is not correct
            else:
                player.setState(dict(
                    score = player.State['score'] - self.board.State['cells'][pck['row']][pck['col']].State['value'],
                ))

                self.setState(dict(
                    wrong_ans = self.State['wrong_ans']+1,
                ))

                send_pck = dict(
                    type = 'QUESTION',
                    turn = self.State['turn'],
                    row = pck['row'],
                    col = pck['col'],
                    question = self.board.State['questions'][pck['row']][pck['col']]['question'],
                    visit = self.board.getVisit(),
                    players = [dict(
                        name = self.State['players'][i].State['name'],
                        score = self.State['players'][i].State['score'],
                    ) for i in range(self.State['allowed_players'])],
                )
                self.broadCast(send_pck)

    def run(self):
        print('Inside game thread')
        self.waitForAllPlayers()

        self.setState(dict(
            gameMode = 'ACTIVE',
        ))


        pck = dict(
            type = 'HAND_SHAKE',
            players_count = self.State['allowed_players'],
            categories = self.board.State['categories'],
            scoresPerCategory = self.board.State['scoresPerCategory'],
            category_columns = self.board.State['category_columns'],
            players = [dict(
                name = self.State['players'][i].State['name'],
                score = self.State['players'][i].State['score'],
            ) for i in range(self.State['allowed_players'])],
        )

        self.broadCastWithId(pck)

        self.setState(dict(
            gameMode = 'RUNNING',
            turn = self.__nextTurn(),
        ))

        pck = dict(
            type = 'PAY_LOAD',
            turn = self.State['turn'],
            visit = self.board.getVisit(),
            players = [dict(
                name = self.State['players'][i].State['name'],
                score = self.State['players'][i].State['score'],
            ) for i in range(self.State['allowed_players'])],
        )

        self.broadCast(pck)

        while self.stopped() == False:
            curr_player = self.State['players'][self.State['turn']]
            pck = curr_player.adapter.recv()
            self.executePck(pck)

        # questionId = 0
        # attr = dict(
        #     query = questions[questionId]['query'],
        #     ansColumn = questions[questionId]['ansColumn'],
        #     userAns = 'Umar Ali Khan',
        # )
        # print(self.checkAns(**attr))
        # self.State['gameMode'] = 'OVER'
        # print(self.State)