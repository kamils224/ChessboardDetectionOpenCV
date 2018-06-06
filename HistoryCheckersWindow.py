import tkinter as tk

from LoadedGameManager import LoadedGameManager
from checkers_board_class import Checkers_Board
from detect import *

gra = LoadedGameManager("SavedGames/trial_game.txt") #wczytaj gre pokazowa


class HistoryCheckersWindow:
    def __init__(self):
        self.actual_round = 0;

        self.HistoryWindow = tk.Toplevel()  # inicjalizacja rooota
        self.HistoryWindow.title("Checkers History")  # tytul okna
        self.HistoryWindow.protocol('WM_DELETE_WINDOW', self.destructor)  # destrucor odpala się po zamknięciu okna

        self.Checkerspanel = tk.Label(self.HistoryWindow).grid(row=0, column=0)





        f1 = tk.Frame(self.HistoryWindow)
        f1.grid(row=1, column=1, sticky="nsew")

        btn = tk.Button(f1, text="move backward", command=self.move_backward)  # przycisk do poprzedniej tury
        btn.config(height=5)
        btn.pack(side="left", fill="both", expand=1, padx=20, pady=20)
        btn = tk.Button(f1, text="move forward", command=self.move_forward)  # przycisk do kolejnej tury
        btn.pack(side="left", fill="both", expand=1, padx=20, pady=20)

        Frame_Slider = tk.Frame(self.HistoryWindow)
        Frame_Slider.grid(row=0, column=2)

        scrollbar = tk.Scrollbar(Frame_Slider)
        # scrollbar.pack(side="right", fill="both", expand=1)
        scrollbar.grid(column=1)

        mylist = tk.Listbox(Frame_Slider, width=2000, height=0, yscrollcommand=scrollbar.set)
        for round_number in gra.game_history:
            mylist.insert(tk.END, str(round_number))

        # mylist.pack(side="right", fill="both", expand=1)
        mylist.grid(column=0)

        scrollbar.config(command=mylist.yview)

    def LoadCheckersBackGround(self):
        szachownica = cv2.imread('Image/szachownica.png')  # wczytanie szablonu , tła do warcab
        self.board_game = Checkers_Board(szachownica, self.Checkerspanel,gra.return_round(0))  # tworzenie nowej gry z histori

    def move_forward(self):
        if self.actual_round < len(gra.game_history) - 1:
            self.actual_round += 1
            self.board_game.draw(gra.return_round(self.actual_round))
        else:
            print("Ostatni ruch")

    def move_backward(self):
        if self.actual_round > 0:
            self.actual_round -= 1
            self.board_game.draw(gra.return_round(self.actual_round))
        else:
            print("Tura 0 ")

    def destructor(self):
        self.HistoryWindow.destroy()