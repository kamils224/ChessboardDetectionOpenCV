from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkfont
from Backend.CheckersVisualization import Checkers_Board
from Backend.BoardDetection import BoardDetection
from Backend.LoadedGameManager import *
import cv2 as cv2


class CaptureCheckersWindow:
    def __init__(self, ip=0,vs=None, output_path="./",):
        if vs==None:
            self.vs = cv2.VideoCapture(ip)
        else:
            self.vs = vs

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

        lista = BoardDetection.Detect()
        Matrix888 = [[0 for x in range(8)] for y in range(8)]

        i =0
        for x in range(0, 8):
            for y in range(0, 8):
                Matrix888[x][y]= lista[i]
                i+=1

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
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors

            new_img = self.rozpoznawania.Detect(frame=frame, detector=self.konfiguracjakamila)

            lista = self.rozpoznawania.result_list
            if new_img is not None:
                cv2.imshow('dwaaa',new_img)

            b = [[0 for x in range(8)] for y in range(8)]
            for y in range(8):
                for x in range(8):
                    if(lista[x+y]==1):
                        ok=2
                    b[x][y] = lista[x+y]
            print(b)

            #print(b)
            self.board_game.draw(b, 0)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA

            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image

        self.root.after(30, self.video_loop)  # call the same function after 30 milliseconds

    def destructor(self):
        self.root.destroy()
        self.vs.release()
