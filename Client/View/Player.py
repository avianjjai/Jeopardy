from tkinter import Canvas, CENTER

class Player:
    def __init__(self, board, height, width, bg, left_x, left_y, name) -> None:
        self.State = dict(
            name = name,
            score = 0
        )
        
        player_attr = dict(
            master = board,
            height = height,
            width = width,
            bg= bg,
        )
        self.playerArea = Canvas(**player_attr)

        nameArea_attr = dict(
            master = self.playerArea,
            height = player_attr['height']/2,
            width = player_attr['width'],
        )
        self.nameArea = Canvas(**nameArea_attr)
        self.nameText = self.nameArea.create_text(width/2, height/4, font=('Helvetica 30 bold'), justify=CENTER)
        self.nameArea.pack()

        scoreArea_attr = dict(
            master = self.playerArea,
            height = player_attr['height']/2,
            width = player_attr['width'],
        )
        self.scoreArea = Canvas(**scoreArea_attr)
        self.scoreText = self.scoreArea.create_text(width/2, height/4, font=('Helvetica 30 bold'), justify=CENTER)
        self.scoreArea.pack()

        self.playerArea.place(x=left_x, y=left_y)
        self.updateState()

    def setState(self, keyValue):
        for key, value in keyValue.items():
            self.State[key] = value
        
        self.updateState()

    def updateState(self):
        self.nameArea.itemconfig(self.nameText, text = self.State['name'])
        self.scoreArea.itemconfig(self.scoreText, text = str(self.State['score']))