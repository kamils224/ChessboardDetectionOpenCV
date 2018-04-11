from PIL import Image, ImageTk
import tkinter as tk
import cv2

from loading_game_class import loading_game
from checkers_board_class import Checkers_Board



gra = loading_game("trial_game.txt") #wczytaj gre pokazowa




class Application:
    def __init__(self, output_path = "./"):
        self.vs = cv2.VideoCapture(1) # klatki z kamerki, 0 to domyślna
        self.output_path = output_path  # sciezka wyjsciowa
        self.current_image = None  # aktualny obraz z kamery
        self.actual_round = 0;

        self.root = tk.Tk()  # inicjalizacja rooota
        self.root.title("Checkers")  # tytul okna
        self.root.protocol('WM_DELETE_WINDOW', self.destructor) # destrucor odpala się po zamknięciu okna

        frameleft = tk.Frame(self.root)
        frameleft.grid(row=0, column=0)

        self.panel = tk.Label(frameleft)  # inicjalizacja panelu z kamera
        self.panel.pack(side="top", fill="both", expand=1)

        self.panel2 = tk.Label(frameleft)
        self.panel2.pack(side="bottom", fill="both", expand=1)


        self.Checkers_panel = tk.Label(self.root)
        self.Checkers_panel.grid(row= 0, column=1)
        szachownica = cv2.imread('Image/szachownica.png')  # wczytanie szablonu , tła do warcab
        self.board_game = Checkers_Board(szachownica, self.Checkers_panel, gra.return_round(0)) #tworzenie nowej gry z histori

        f1 = tk.Frame(self.root)
        f1.grid(row=1, column=1, sticky="nsew")

        btn = tk.Button(f1, text="move backward", command=self.move_backward) # przycisk do poprzedniej tury
        btn.config(height=5)
        btn.pack(side="left", fill="both", expand=1, padx=20, pady=20)
        btn = tk.Button(f1, text="move forward", command=self.move_forward)  # przycisk do kolejnej tury
        btn.pack(side="left", fill="both", expand=1, padx=20, pady=20)

        f2 = tk.Frame(self.root)
        f2.grid(row=1, column=0, sticky="nsew")

        Frame_Slider = tk.Frame(self.root)
        f1.grid(row=0, column=2)

        scrollbar = tk.Scrollbar(Frame_Slider)
        scrollbar.pack(side="right", fill="y")

        mylist = tk.Listbox(Frame_Slider, yscrollcommand=scrollbar.set)
        for round_number in gra.game_history:
            mylist.insert(tk.END, str(round_number) + "This is round number ")

        mylist.pack(side="left", fill="both")
        scrollbar.config(command=mylist.yview)

        self.video_loop()

    def Slider_function(self,val):
        print(val)


    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA

            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image


            imgtk2 = cv2.resize(cv2.Canny(cv2image, 100, 200),(400,400))


            wow = Image.fromarray(imgtk2)
            imgtk2 = ImageTk.PhotoImage(image=wow)
            self.panel2.imgtk = imgtk2  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel2.config(image=imgtk2)  # show the image

        self.root.after(30, self.video_loop)  # call the same function after 30 milliseconds

    def move_forward(self):
        if self.actual_round < len(gra.game_history) - 1:
            self.actual_round +=1
            self.board_game.draw(gra.return_round(self.actual_round))
        else:
            print("Ostatni ruch")

    def move_backward(self):
        if self.actual_round > 0 :
            self.actual_round -=1
            self.board_game.draw(gra.return_round(self.actual_round))
        else:
            print("Tura 0 ")

    def destructor(self):
        self.root.destroy()
        self.vs.release()


pba = Application()
pba.root.mainloop()