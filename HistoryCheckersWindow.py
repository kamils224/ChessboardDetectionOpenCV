import tkinter as tk
from checkers_board_class import Checkers_Board
import tkinter.font as tkfont
from detect import *



class HistoryCheckersWindow:
    def __init__(self, gra):
        self.actual_round = 0;
        self.gra = gra
        self.HistoryWindow = tk.Toplevel()  # inicjalizacja rooota
        self.helv36 = tkfont.Font(family='Helvetica', size=15, weight='bold')
        self.HistoryWindow.title("Checkers History")  # tytul okna
        self.HistoryWindow.protocol('WM_DELETE_WINDOW', self.destructor)  # destrucor odpala się po zamknięciu okna
        self.Checkerspanel = tk.Label(self.HistoryWindow)
        self.Checkerspanel.grid(row=0, column=0)
        self.LoadCheckersBackground()
        self.InitializeButtons()
        self.InitializeHistoryList()


    def onselect(self,evt):
        index = int(evt.widget.curselection()[0])
        self.actual_round = index-1
        self.move_forward()


    def InitializeHistoryList(self):
        RightFrame = tk.Frame(self.HistoryWindow,width =10)
        RightFrame.grid(row=0, column=2)


        scrollbar = tk.Scrollbar(RightFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mylist = tk.Listbox(RightFrame,  width=50, height=20,  yscrollcommand=scrollbar.set, font=self.helv36)
        self.mylist.bind('<<ListboxSelect>>', self.onselect)

        x = 0
        while x < len(self.gra.game_history):
            self.mylist.insert(tk.END, "Runda " + str(x))
            x+=1

            self.mylist.pack( side = tk.LEFT)

        self.mylist.select_set(self.actual_round)
        scrollbar.config(command=self.mylist.yview)

    def InitializeButtons(self):
        f1 = tk.Frame(self.HistoryWindow)
        f1.grid(row=1, column=1, sticky="nsew")

        btn = tk.Button(f1, text="Cofnij", command=self.move_backward,font=self.helv36)  # przycisk do poprzedniej tury
        btn.config(height=2)
        btn.pack(side="left", fill="both", expand=1, padx=5, pady=10)
        btn = tk.Button(f1, text="Dalej", command=self.move_forward, font=self.helv36)  # przycisk do kolejnej tury
        btn.pack(side="left", fill="both", expand=1, padx=5, pady=10)

    def LoadCheckersBackground(self):
        szachownica = cv2.imread('Image/szachownica.png')  # wczytanie szablonu , tła do warcab
        self.board_game = Checkers_Board(szachownica, self.Checkerspanel,
                                         self.gra.return_round(0))  # tworzenie nowej gry z histori

    def move_forward(self):
        if self.actual_round < len(self.gra.game_history) - 1:
            self.actual_round += 1
            self.board_game.draw(self.gra.return_round(self.actual_round),0)
            self.mylist.get(self.actual_round)
            self.mylist.select_clear(0,len(self.gra.game_history))
            self.mylist.select_set(self.actual_round)
        else:
            print("Ostatni ruch")

    def move_backward(self):
        if self.actual_round > 0:
            self.actual_round -= 1
            self.board_game.draw(self.gra.return_round(self.actual_round),0)
            self.mylist.get(self.actual_round)
            self.mylist.select_clear(0, len(self.gra.game_history))
            self.mylist.select_set(self.actual_round)
        else:
            print("Tura 0 ")

    def destructor(self):
        self.HistoryWindow.destroy()