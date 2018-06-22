from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkfont
from Backend.CheckersVisualization import Checkers_Board
from Backend.BoardDetection import BoardDetection
from Backend.LoadedGameManager import *
import cv2 as cv2
import threading



class CaptureCheckersWindow:
    def __init__(self, ip=0,vs=None, output_path="./",):
        #self.cap = cv2.VideoCapture(ip)

        self.rozpoznawania = BoardDetection()
        self.konfiguracjakamila = self.rozpoznawania.ConfigureBlobDetector()


        self.output_path = output_path  # sciezka wyjsciowa
        self.current_image = None  # aktualny obraz z kamery
        self.actual_round = 0;

        self.root = tk.Toplevel()  # inicjalizacja rooota
        self.root.title("Checkers")  # tytul okna
        self.root.protocol('WM_DELETE_WINDOW', self.destructor) # destrucor odpala się po zamknięciu okna

        self.frameleft = tk.Frame(self.root)
        self.frameleft.grid(row=0, column=0)

        self.panel = tk.Label(self.frameleft)  # inicjalizacja panelu z kamera
        self.panel.pack(side="top", fill="both", expand=1)

        self.panel2 = tk.Label(self.frameleft)
        self.panel2.pack(side="bottom", fill="both", expand=1)

        self.Checkers_panel = tk.Label(self.root)
        self.Checkers_panel.grid(row=0, column=1)

        self.gra = LoadedGameManager("SavedGames/trial_game.txt")
        szachownica = cv2.imread('Image/szachownica.png')
        self.board_game = Checkers_Board(szachownica, self.Checkers_panel, self.gra.return_round(0))

        self.Initialize()
        szachownica = cv2.imread('Image/szachownica.png')  # wczytanie szablonu , tła do warcab

        Matrix888 = [[0 for x in range(8)] for y in range(8)]

        self.board_game = Checkers_Board(szachownica, self.Checkers_panel, Matrix888)

        self.video_loop()

    def Initialize(self):
        helv36 = tkfont.Font(family='Helvetica', size=15, weight='bold')

        player1 = tk.Button(self.frameleft, text="Wykonaj Ruch", command=self.Catch,
                            font=helv36).pack(side="bottom", fill="both", expand=1)

        tk.Label(self.frameleft, text="Niebieski").pack(side="bottom", fill="both", expand=1)

        tk.Label(self.frameleft, text="Czerwony").pack(side="bottom", fill="both", expand=1)

    def Catch(self):
        self.rozpoznawania.button_clicked=True
        print (self.rozpoznawania.result_list)


    def video_loop(self):

        t=threading.Thread(target=self.rozpoznawania.StartDetection)
        t.start()
        #self.rozpoznawania.StartDetection()

    def destructor(self):
        self.root.destroy()
        self.vs.release()
