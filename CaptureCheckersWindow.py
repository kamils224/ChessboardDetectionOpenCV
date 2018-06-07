from PIL import Image, ImageTk
import tkinter as tk

from checkers_board_class import Checkers_Board
from detect import *


class CaptureCheckersWindow:
    def __init__(self, ip=0,vs=None, output_path="./",):
        if vs==None:
            self.vs = cv2.VideoCapture(ip)
        else:
            self.vs = vs

        self.output_path = output_path  # sciezka wyjsciowa
        self.current_image = None  # aktualny obraz z kamery
        self.actual_round = 0;

        self.root = tk.Toplevel()  # inicjalizacja rooota
        self.root.title("Checkers")  # tytul okna
        self.root.protocol('WM_DELETE_WINDOW', self.destructor) # destrucor odpala się po zamknięciu okna

        frameleft = tk.Frame(self.root)
        frameleft.grid(row=0, column=0)

        self.panel = tk.Label(frameleft)  # inicjalizacja panelu z kamera
        self.panel.pack(side="top", fill="both", expand=1)

        self.panel2 = tk.Label(frameleft)
        self.panel2.pack(side="bottom", fill="both", expand=1)

        self.Checkers_panel = tk.Label(self.root)
        self.Checkers_panel.grid(row=0, column=1)

        szachownica = cv2.imread('Image/szachownica.png')  # wczytanie szablonu , tła do warcab

        lista = DetectBoard()
        Matrix888 = [[0 for x in range(8)] for y in range(8)]

        i =0
        for x in range(0, 8):
            for y in range(0, 8):
                Matrix888[x][y]= lista[i]
                i+=1

        self.board_game = Checkers_Board(szachownica, self.Checkers_panel, Matrix888)

        self.video_loop()

    def video_loop(self):
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA

            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image

        self.root.after(30, self.video_loop)  # call the same function after 30 milliseconds

    def destructor(self):
        self.root.destroy()
        self.vs.release()
