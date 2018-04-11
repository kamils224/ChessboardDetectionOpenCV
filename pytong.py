import copy
import json
from PIL import Image, ImageTk
import tkinter as tk
import cv2


class old_play(): #klasa przechowującą zapisaną rozgrywkę
    def __init__(self,path):
        self.path = path
        self.load()

    def load(self): #wczytywanie z pliku JSON historie rozgrywki, nazwa, historia
        data = open(self.path, 'r').read()
        parsed_json = json.loads(data)
        self.game_name = parsed_json["game_name"]
        self.json_game_history = parsed_json["game_history"]

    def return_round(self, round_number): # zwraca macierz obrazującą plansze w danej rundzie,
        if round_number >= len(self.json_game_history):
            print("W historii nie ma takiej rundy")
        else:
            return self.json_game_history[round_number]["pawns"]

gra = old_play('trial_game.txt')



class Checkers_Board(): # klasa zajmująca się wizualizacją

    def __init__(self, image_board, visualisation, start_position):
        self.sprite = image_board # sprite - tło
        self.board = copy.deepcopy(self.sprite) # na tym jest rysowana jedna klatka
        self.Matrix = start_position
        self.visualisation = visualisation
        self.draw(start_position)


    def draw(self,PositionMatrix):
        self.board = copy.deepcopy(self.sprite)
        for x in range(len(self.Matrix)):
            for y in range(len(self.Matrix[x])):
                if self.Matrix[y][x] != PositionMatrix[y][x]:
                    if PositionMatrix[y][x] > 0 :
                        cv2.rectangle(self.board, (2+(x * 100), 2+(y * 100)), (98+(x * 100), 98+(y * 100)), (0, 255, 0), 4)
                    else:
                        cv2.rectangle(self.board, (2 + (x * 100), 2 + (y * 100)), (98 + (x * 100), 98 + (y * 100)),(0, 0, 255), 4)
                if PositionMatrix[y][x] == 0:
                    continue
                elif PositionMatrix[y][x] == 1:
                    cv2.circle(self.board, (50 + (x * 100), 50 + (y * 100)), 40, (200,113,19), -1)
                elif PositionMatrix[y][x] == 2:
                    cv2.circle(self.board, (50 + (x * 100), 50 + (y * 100)), 40, (0, 0, 255), -1)
                elif PositionMatrix[y][x] == 3:
                    cv2.circle(self.board, (50 + (x * 100), 50 + (y * 100)), 40, (200,113,19), -1)
                    cv2.circle(self.board, (50 + (x * 100), 50 + (y * 100)), 30, (150,113,19), -1)
                elif PositionMatrix[y][x] == 4:
                    cv2.circle(self.board, (50 + (x * 100), 50 + (y * 100)), 40, (0, 0, 100), -1)
                    cv2.circle(self.board, (50 + (x * 100), 50 + (y * 100)), 30, (0, 0, 255), -1)

        b, g, r = cv2.split(self.board)
        image = cv2.merge((r, g, b))
        image2 = Image.fromarray(image)
        tura8 = ImageTk.PhotoImage(image=image2)
        self.visualisation.configure(image=tura8)
        self.visualisation.image = tura8
        self.visualisation.grid(row= 0, column=1)
        self.Matrix = PositionMatrix


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
        szachownica = cv2.imread('szachownica.png')  # wczytanie szablonu , tła do warcab
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
        for round_number in gra.json_game_history:
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
        if self.actual_round < len(gra.json_game_history) - 1:
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