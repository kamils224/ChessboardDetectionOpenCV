from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkfont
import cv2

from CaptureCheckersWindow import CaptureCheckersWindow
from HistoryCheckersWindow import HistoryCheckersWindow

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
        photo = cv2.imread('Image/background_main.png')

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
                                 font=helv36).grid(row=0, column=0, padx=(250, 250), pady=(230, 0))

        self.button2 = tk.Button(self.background, text="Wczytaj z Historii", command=self.RunHistoryCheckers,
                                 font=helv36).grid(row=1, column=0, padx=(250, 250), pady=(50, 230))

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
        Capture = CaptureCheckersWindow()

    def RunHistoryCheckers(self):
        History = HistoryCheckersWindow()