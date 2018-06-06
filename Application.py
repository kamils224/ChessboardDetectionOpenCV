from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkfont
import cv2

from HistoryCheckersWindow import HistoryCheckersWindow
from Options import OptionsClass

class Application:
    def __init__(self):
        self.create_window()
        self.load_background()
        self.create_buttons()

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
                                 font=helv36).grid(row=1, column=0, padx=(250, 250), pady=(35, 160))

    def RunCaptureCheckers(self):
        Capture = OptionsClass()

    def RunHistoryCheckers(self):
        History = HistoryCheckersWindow()