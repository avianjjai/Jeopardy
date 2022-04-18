from cgitb import text
from tkinter import Canvas, CENTER

class Cell:
    def __init__(self, board, height, width, bg, left_x, left_y, row, col, selectQuestion) -> None:
        self.State = dict(
            row = row,
            col = col,
            value = (row+1)*200,
            visit = False,
        )
        self.selectQuestion = selectQuestion
        
        cell_attr = dict(
            master = board,
            height = height,
            width = width,
            cursor = 'target',
            bg= bg,
        )
        self.cell = Canvas(**cell_attr)
        
        self.text = self.cell.create_text(width/2, height/2, text='', fill='black', font=('Helvetica 30 bold'), justify=CENTER)
        
        self.cell.bind('<Button-1>', lambda e: self.selectQuestion(self))
        self.cell.place(x=left_x, y=left_y)
        self.updateState()

    def setState(self, keyValue):
        for key, value in keyValue.items():
            self.State[key] = value
        
        self.updateState()


    def updateState(self):
        if not self.State['visit']:
            self.cell.itemconfig(self.text, text=str(self.State['value']) + '$')
        else:
            self.cell.itemconfig(self.text, text = '')


    def click_cell(self):
        if self.State['isActive']():
            self.setState(dict(
                visit = True,
            ))
            self.updateState()


class SimpleCell:
    def __init__(self, board, height, width, bg, left_x, left_y, text) -> None:        
        self.State = dict(
            text = text
        )
        
        cell_attr = dict(
            master = board,
            height = height,
            width = width,
            bg= bg,
        )
        self.cell = Canvas(**cell_attr)
        
        self.text = self.cell.create_text(width/2, height/2, text='', fill='black', font=('Helvetica 30 bold'), justify=CENTER)
        
        self.cell.place(x=left_x, y=left_y)
        self.updateState()


    def updateState(self):
        self.cell.itemconfig(self.text, text=self.State['text'])