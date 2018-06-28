import tkinter as tk
import tkinter.font as tkfont
from Backend.SaveGame import SaveGame

class GetParameterToSaveFile:
    def __init__(self, parent,gamehistory):
        self.gameHistory = gamehistory
        self.helv36 = tkfont.Font(family='Helvetica', size=12, weight='bold')
        top = self.top = tk.Toplevel(parent)
        self.top.title("Zapisywanie rozgrywki")

        self.game_name = tk.StringVar(top, value='')
        self.player1_name = tk.StringVar(top, value='')
        self.player2_name = tk.StringVar(top, value='')

        tk.Label(top, text="Nazwa gry").grid(row=0, column=0)
        tk.Entry(top, width=25, textvariable=self.game_name,
                 font=self.helv36).grid(row=0, column=1)

        tk.Label(top, text="Pseudonim gracza 1").grid(row=1, column=0)
        tk.Entry(top, width=25, textvariable=self.player1_name,
                 font=self.helv36).grid(row=1, column=1)

        tk.Label(top, text="Pseudonim gracza 2").grid(row=2, column=0)
        tk.Entry(top, width=25, textvariable=self.player2_name
                 , font=self.helv36).grid(row=2, column=1)

        tk.Button(top, text='Zapisz rozgrywke', command=self.ok,
                  font=self.helv36).grid(row=3, column=1)

    def ok(self):
        SaveGame(self.gameHistory, gamename=self.game_name.get(), p1name=self.player1_name.get(), p2name=self.player2_name.get())
        self.top.destroy()



