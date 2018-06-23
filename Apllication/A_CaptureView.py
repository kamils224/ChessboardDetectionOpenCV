from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkfont
from Backend.CheckersVisualization import Checkers_Board
from Backend.BoardDetection import BoardDetection
from Backend.LoadedGameManager import *
import cv2 as cv2
import threading



class CaptureCheckersWindow:
    def __init__(self, ip=0):
        self.rozpoznawania = BoardDetection()
        self.rozpoznawania.video_device=ip
        self.root = tk.Toplevel()  # inicjalizacja rooota
        self.root.title("Checkers")  # tytul okna
        self.root.protocol('WM_DELETE_WINDOW', self.destructor) # destrucor odpala się po zamknięciu okna

        self.Checkers_panel = tk.Label(self.root)
        self.Checkers_panel.grid(row=0, column=0)

        self.UserFrame = tk.Frame(self.root)
        self.UserFrame.grid(row=1, column=1)

        self.panel2 = tk.Label(self.UserFrame)
        self.panel2.pack(side="bottom", fill="both", expand=1)

        self.DeafaultBoard()

        self.video_loop()

    def DeafaultBoard(self):
        self.Initialize()
        szachownica = cv2.imread('Image/szachownica.png')  # wczytanie szablonu , tła do warcab
        Matrix888 = [[0 for x in range(8)] for y in range(8)]
        self.board_game = Checkers_Board(szachownica, self.Checkers_panel, Matrix888)

    def Initialize(self):
        helv36 = tkfont.Font(family='Helvetica', size=15, weight='bold')

        player1 = tk.Button(self.panel2, text="Wykonaj Ruch", command=self.Catch,
                            font=helv36).pack(side="bottom", fill="both", expand=1)
        tk.Label(self.panel2, text="Niebieski").pack(side="bottom", fill="both", expand=1)
        tk.Label(self.panel2, text="Czerwony").pack(side="bottom", fill="both", expand=1)

    def Catch(self):
        plansza = self.rozpoznawania.result_list
        print(plansza)
        MatrixDraw = [[0 for x in range(8)] for y in range(8)]
        i = 0
        for x in range(0, 8):
            for y in range(0, 8):
                 MatrixDraw[x][y] = plansza[i]
                 i += 1

        print(MatrixDraw)
        self.board_game.draw(MatrixDraw,0)

    def video_loop(self):
        t=threading.Thread(target=self.rozpoznawania.StartDetection)
        t.start()

    def destructor(self):
        self.root.destroy()
