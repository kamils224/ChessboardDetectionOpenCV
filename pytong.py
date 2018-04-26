from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkfont
import cv2



from my_class.loading_game_class import loading_game
from my_class.checkers_board_class import Checkers_Board
from my_class.detect import *

gra = loading_game("games/trial_game.txt") #wczytaj gre pokazowa

class CaptureCheckersWindow:
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
        #self.board_game = Checkers_Board(szachownica, self.Checkers_panel, gra.return_round(0)) #tworzenie nowej gry z histori


        lista =DetectBoard()
        Matrix888 = [[0 for x in range(8)] for y in range(8)]

        i =0
        for x in range(0, 8):
            for y in range(0, 8):
                Matrix888[x][y]= lista[i]
                i+=1

        self.board_game = Checkers_Board(szachownica, self.Checkers_panel,Matrix888)

        f1 = tk.Frame(self.root)
        f1.grid(row=1, column=1, sticky="nsew")

        btn = tk.Button(f1, text="move backward", command=self.move_backward) # przycisk do poprzedniej tury
        btn.config(height=5)
        btn.pack(side="left", fill="both", expand=1, padx=20, pady=20)
        btn = tk.Button(f1, text="move forward", command=self.move_forward)  # przycisk do kolejnej tury
        btn.pack(side="left", fill="both", expand=1, padx=20, pady=20)


        Frame_Slider = tk.Frame(self.root)
        Frame_Slider.grid(row=0, column=2)

        scrollbar = tk.Scrollbar(Frame_Slider)
        #scrollbar.pack(side="right", fill="both", expand=1)
        scrollbar.grid(column = 1)


        mylist = tk.Listbox(Frame_Slider, width=2000, height=0, yscrollcommand=scrollbar.set)
        for round_number in gra.game_history:
            mylist.insert(tk.END, str(round_number))

        #mylist.pack(side="right", fill="both", expand=1)
        mylist.grid(column= 0)

        scrollbar.config(command=mylist.yview)



        self.video_loop()

    def Slider_function(self, val):
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


class Application:
    def __init__(self):

        self.create_window()
        self.load_background()
        self.create_buttons()
        self.create_menu()

    def create_window(self):
        self.root = tk.Tk()  # inicjalizacja rooota
        self.root.title("Checkers")  # tytul okna

    def load_background(self):
        self.background = tk.Label(self.root, compound=tk.CENTER)
        photo = cv2.imread('Image/background_main.gif')

        b, g, r = cv2.split(photo)
        image = cv2.merge((r, g, b))
        image2 = Image.fromarray(image)
        tura8 = ImageTk.PhotoImage(image=image2)
        self.background.configure(image=tura8)
        self.background.image = tura8
        self.background.grid(row=0, column=0)

    def create_buttons(self):
        helv36 = tkfont.Font(family='Helvetica', size=15, weight='bold')

        self.button1 = tk.Button(self.background, text="Przechwytywanie z Kamery", command=self.RunCaptureCheckers,
                                 font=helv36)
        self.button1.grid(row=0, column=0, padx=(250, 250), pady=(230, 0))

        self.button2 = tk.Button(self.background, text="Wczytaj z Historii", command=self.RunHistoryCheckers,
                                 font=helv36)
        self.button2.grid(row=1, column=0, padx=(250, 250), pady=(50, 230))

    def create_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_command(label="Save as...", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)


        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

    def donothing(self):
        filewin = tk.Toplevel(self.root)
        button = tk.Button(filewin, text="Do nothing button")
        button.pack()

    def RunCaptureCheckers(self):
        filewin = tk.Toplevel(self.root)
        filewin.title("Capture Checkers")
        print("RunCaptureCheckers")

    def RunHistoryCheckers(self):
        print("RunHistoryCheckers")



#pba = CaptureCheckersWindow()
#pba.root.mainloop()

okno = Application()
okno.root.mainloop()