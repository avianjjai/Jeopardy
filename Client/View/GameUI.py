from tkinter import Button, Canvas, CENTER, Tk
from View.QuestionUI import QuestionUI
from View.Cell import Cell, SimpleCell
from View.Player import Player
from Data.Data import lock

class GameUI:
    def __init__(self, master, width: float, height: float, bg, players_count, players, id, sendBuffer, categories, scoresPerCategory, category_columns) -> None:
        self.State = dict(
            round = 0,
            turn = -1,
            active = False,
            players_count = players_count,
            players = [],
            exit_button_state = 'active',
            submit_button_state = 'active',
            id = id,
            sendBuffer = sendBuffer,
            categories = categories,
            scoresPerCategory = scoresPerCategory,
            category_columns = category_columns,
            questionAnswer = dict(
                row = -1,
                col = -1,
                question = '',
                answer = '',
            ),
        )

        self.master = master
        self.master.title('JeoPardy Game')
        dimension = str(width) + 'x' + str(height)
        self.master.geometry(dimension)

        # Complete IDE
        canvas = dict(
            master = self.master,
            height = height,
            width = width,
            bg = bg,
        )
        self.canvas = Canvas(**canvas)

        self.round_no = 0

        # Round No. Area
        round_attr = dict(
            master = self.canvas,
            height = canvas['height']*0.1,
            width = canvas['width'],
            bg = '#123456',
        )
        self.roundArea = Canvas(**round_attr)

        self.round = self.roundArea.create_text(round_attr['width']/2, round_attr['height']/2, fill='black', font=('Helvetica 30 bold'), justify=CENTER)
        
        self.roundArea.pack()

        # Player_description
        player_attr = dict(
            master = self.canvas,
            height = canvas['height']*0.15,
            width = canvas['width'],
            bg = '#234567',
        )
        self.playerArea = Canvas(**player_attr)

        left_x = 0
        left_y = 0
        for i in range(self.State['players_count']):
            attr = dict(
                board = self.playerArea,
                width = player_attr['width']/self.State['players_count'],
                height = player_attr['height'],
                bg = '#459894',
                left_x = left_x,
                left_y = left_y,
                name = players[i]['name'],
            )
            self.State['players'].append(Player(**attr))
            left_x += attr['width']
        
        self.playerArea.pack()

        # Turn Area
        turn_attr = dict(
            master = self.canvas,
            height = canvas['height']*0.1,
            width = canvas['width'],
            bg = '#345678',
        )
        self.turnArea = Canvas(**turn_attr)
        self.turnText = self.turnArea.create_text(turn_attr['width']/2, turn_attr['height']/2, font=('Helvetica 30 bold'), justify=CENTER)
        self.turnArea.pack()


        # Question Answer Area
        questionAnswer_attr = dict(
            master = self.canvas,
            width = canvas['width'],
            height = canvas['height']*0.2,
            question_window_state = 'disabled',
            question = '',
            answer = '',
            bg = '#B49D98',
        )
        self.questionAnswer = QuestionUI(**questionAnswer_attr)

        # Board Outer Area
        board_attr_outer = dict(
            master = self.canvas,
            height = canvas['height']*0.35,
            width = canvas['width'],
            bg = '#456789',
        )
        self.boardAreaOuter = Canvas(**board_attr_outer)

        # Board Area
        board_attr = dict(
            master = self.boardAreaOuter,
            height = board_attr_outer['height'],
            width = board_attr_outer['width']-100,
            bg = '#135791',
        )
        self.boardArea = Canvas(**board_attr)

        no_of_categories = self.State['categories']
        columns = self.State['category_columns']
        no_of_rows = self.State['scoresPerCategory']+1
        cell_h = board_attr['height']/no_of_rows
        cell_w = board_attr['width']/no_of_categories

        self.categeriesCells = []

        self.cells = [[None for i in range(no_of_categories)] for j in range(no_of_rows)]
        for i in range(no_of_rows):
            if i == 0:
                for j in range(no_of_categories):
                    cell_attr = dict(
                        board = self.boardArea,
                        height = cell_h,
                        width = cell_w,
                        bg = '#868597',
                        left_x = cell_w*j,
                        left_y = cell_h*i,
                        text = columns[j],
                    )
                    self.categeriesCells.append(SimpleCell(**cell_attr))
            
            else:
                for j in range(no_of_categories):
                    cell_attr = dict(
                        board = self.boardArea,
                        height = cell_h,
                        width = cell_w,
                        bg = '#868597',
                        left_x = cell_w*j,
                        left_y = cell_h*i,
                        row = i-1,
                        col = j,
                        selectQuestion = self.selectQuestion,
                    )
                    self.cells[i-1][j] = Cell(**cell_attr)
        
        self.boardArea.pack()

        self.boardAreaOuter.pack()

        # Control Area
        control_attr = dict(
            master = self.canvas,
            height = canvas['height']*0.1,
            width = canvas['width'],
            bg = '#567890',
        )
        self.controlArea = Canvas(**control_attr)
        
        # Button-1 Area
        button_1_attr = dict(
            master = self.controlArea,
            width = control_attr['width']*0.33,
            height = control_attr['height']-10,
            bg = '#901234',
        )
        self.button1Area = Canvas(**button_1_attr)

        submit_button_attr = dict(
            master = self.button1Area,
            padx = 20,
            pady = 10,
            text = 'Submit',
            font=('Helvetica', 15, 'bold'),
            command = self.submit,
        )
        self.submitButton = Button(**submit_button_attr)
        self.submitButton.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.button1Area.place(x = 0, y = 0)

        # Button-2 Area
        button_2_attr = dict(
            master = self.controlArea,
            width = control_attr['width']*0.33,
            height = control_attr['height']-10,
            bg = '#012345',
        )
        self.button2Area = Canvas(**button_2_attr)
        self.button2Area.place(x = button_1_attr['width'], y = 0)

        # Button-3 Area
        button_3_attr = dict(
            master = self.controlArea,
            width = control_attr['width']*0.338,
            height = control_attr['height']-10,
            bg = '#123456',
        )
        self.button3Area = Canvas(**button_3_attr)

        exit_button_attr = dict(
            master = self.button3Area,
            padx = 20,
            pady = 10,
            text = 'Exit',
            font=('Helvetica', 15, 'bold'),
            command = self.exit,
        )
        self.exitButton = Button(**exit_button_attr)
        self.exitButton.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.button3Area.place(x = button_1_attr['width'] + button_2_attr['width'], y = 0)

        self.controlArea.pack()

        self.canvas.pack()
        self.setState(dict())

    def setVisit(self, visit):
        for row in range(len(visit)):
            for col in range(len(visit[0])):
                self.cells[row][col].setState(dict(
                    visit = visit[row][col],
                ))

    def setPlayer(self, players):
        for i in range(self.State['players_count']):
            player = self.State['players'][i]
            player.setState(dict(
                name = players[i]['name'],
                score = players[i]['score']
            ))

    def getVisit(self):
        visit = []
        for row in range(self.State['scoresPerCategory']):
            visit.append([])
            for col in range(self.State['categories']):
                visit[-1].append(self.cells[row][col].State['visit'])

        return visit

    def selectQuestion(self, cell):
        if self.State['active'] and cell.State['visit'] == False:
            self.setState(dict(
                active = False,
            ))

            cell.setState(dict(
                visit = True,
            ))

            pck = dict(
                type = 'REQUEST_QUESTION',
                visit = self.getVisit(),
                row = cell.State['row'],
                col = cell.State['col'],
            )

            print(pck)

            lock.acquire()
            self.State['sendBuffer'].append(pck)
            lock.release()

    def isActive(self):
        return self.State['active']

    def setState(self, keyValue):
        for key, value in keyValue.items():
            self.State[key] = value
        
        self.updateState()

    def submit(self):
        self.State['questionAnswer']['answer'] = self.questionAnswer.answerBox.get(1.0, 'end-1c')
        self.questionAnswer.setState(dict(
            question = '',
            question_window_state = 'disabled',
        ))
        self.submitButton.configure(state='disabled')

        pck = dict(
            type = 'ANSWER',
            row = self.State['questionAnswer']['row'],
            col = self.State['questionAnswer']['col'],
            answer = self.State['questionAnswer']['answer'],
            visit = self.getVisit(),
        )

        lock.acquire()
        self.State['sendBuffer'].append(pck)
        lock.release()

        

    def exit(self):
        pck = dict(
            type = 'FIN',
        )

        lock.acquire()
        self.State['sendBuffer'].append(pck)
        lock.release()

    def destroy(self):
        self.master.destroy()

    def updateState(self):
        self.roundArea.itemconfig(self.round, text='Round - ' + str(self.State['round']))
        if self.State['turn'] == -1:
            self.turnArea.itemconfig(self.turnText, text = 'Turn: ')
        else:
            self.turnArea.itemconfig(self.turnText, text = 'Turn: ' + self.State['players'][self.State['turn']].State['name'])
        for player in self.State['players']:
            player.updateState()

        self.submitButton.config(state=self.State['submit_button_state'])
        self.exitButton.config(state=self.State['exit_button_state'])
    def endGame(self):
        pass