from tkinter import Tk
from View.GameUI import GameUI
from Connection.Adapter import Adapter
from Data.ServerData import SERVER_IDENTITY
from Controller.GameController import GameController

def Initialize():
    gameController = GameController()
    gameController.start()
    print('Initialize.py Closed')