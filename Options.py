from PIL import Image, ImageTk
import tkinter as tk

from checkers_board_class import Checkers_Board
from detect import *


class OptionsClass:
    def __init__(self, output_path = "./"):
        self.vs = cv2.VideoCapture(0) # klatki z kamerki, 0 to domyślna
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

        self.Options_panel = tk.Label(self.root)
        self.Options_panel.grid(row=0, column=1)


        Frame_Slider = tk.Frame(self.Options_panel)
        Frame_Slider.grid(row=0, column=2)
        w = tk.Scale(Frame_Slider, from_= 0, to=255, orient='horizontal')    #tutaj przykład masz !!! -------
        w.pack()
        w = tk.Scale(Frame_Slider, from_= 0, to=255, orient='horizontal')
        w.pack()
        w = tk.Scale(Frame_Slider, from_=0, to=255, orient='horizontal')
        w.pack()
        w = tk.Scale(Frame_Slider, from_=0, to=255, orient='horizontal')
        w.pack()
        w = tk.Scale(Frame_Slider, from_=0, to=255, orient='horizontal')
        w.pack()
        w = tk.Scale(Frame_Slider, from_=0, to=255, orient='horizontal')
        w.pack()
        w = tk.Scale(Frame_Slider, from_=0, to=255, orient='horizontal')
        w.pack()
        w = tk.Scale(Frame_Slider, from_=0, to=255, orient='horizontal')
        w.pack()




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
