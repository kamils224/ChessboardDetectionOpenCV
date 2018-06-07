import tkinter as tk
from checkers_board_class import Checkers_Board
from detect import *

class HistoryCheckersWindow:
    def __init__(self, gra):
        self.actual_round = 0;
        self.gra = gra
        self.HistoryWindow = tk.Toplevel()  # inicjalizacja rooota
        self.HistoryWindow.title("Checkers History")  # tytul okna
        self.HistoryWindow.protocol('WM_DELETE_WINDOW', self.destructor)  # destrucor odpala się po zamknięciu okna
        self.Checkerspanel = tk.Label(self.HistoryWindow)
        self.Checkerspanel.grid(row=0, column=0)
        self.LoadCheckersBackground()
        self.InitializeButtons()
        self.InitializeHistoryList()

    def InitializeHistoryList(self):


        RightFrame = tk.Frame(self.HistoryWindow)
        RightFrame.grid(row=0, column=2)
        scrollbar = tk.Scrollbar(RightFrame)

        mylist = tk.Listbox(RightFrame, width=100, height=0,  yscrollcommand=scrollbar.set)


        x = 0
        while x < len(self.gra.game_history):
            mylist.insert(tk.END, "Runda " + str(x))
            x+=1

        mylist.grid(column=0)

        scrollbar.config(command=mylist.yview)


    def InitializeButtons(self):
        f1 = tk.Frame(self.HistoryWindow)
        f1.grid(row=1, column=1, sticky="nsew")

        btn = tk.Button(f1, text="move backward", command=self.move_backward)  # przycisk do poprzedniej tury
        btn.config(height=5)
        btn.pack(side="left", fill="both", expand=1, padx=20, pady=20)
        btn = tk.Button(f1, text="move forward", command=self.move_forward)  # przycisk do kolejnej tury
        btn.pack(side="left", fill="both", expand=1, padx=20, pady=20)


    def LoadCheckersBackground(self):
        szachownica = cv2.imread('Image/szachownica.png')  # wczytanie szablonu , tła do warcab
        self.board_game = Checkers_Board(szachownica, self.Checkerspanel,
                                         self.gra.return_round(0))  # tworzenie nowej gry z histori

    def move_forward(self):
        if self.actual_round < len(self.gra.game_history) - 1:
            self.actual_round += 1
            self.board_game.draw(self.gra.return_round(self.actual_round))
        else:
            print("Ostatni ruch")

    def move_backward(self):
        if self.actual_round > 0:
            self.actual_round -= 1
            self.board_game.draw(self.gra.return_round(self.actual_round))
        else:
            print("Tura 0 ")

    def destructor(self):
        self.HistoryWindow.destroy()