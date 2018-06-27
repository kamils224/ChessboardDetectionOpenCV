from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkfont
from Apllication.A_CaptureView import CaptureCheckersWindow
from Backend.BoardDetection import *


class OptionsClass:
    def __init__(self):
        self.CreateOptionWindow()

    def CreateOptionWindow(self):
        self.helv36 = tkfont.Font(family='Helvetica', size=12, weight='bold')
        self.OptionsWindow = tk.Toplevel()  # inicjalizacja rooota
        self.OptionsWindow.title("Camera IP")  # tytul okna
        self.CameraIP = tk.StringVar(self.OptionsWindow, value='http://192.168.0.100:4747/video%27')
        self.InitializePanels()
        self.center()

    def InitializePanels(self):
        self.RightPanel = tk.Label(self.OptionsWindow)
        self.RightPanel.grid(row=0, column=1)
        tk.Entry(self.RightPanel, width=50 , textvariable=self.CameraIP, font=self.helv36)\
            .grid(row=1, column=2, pady=10, padx=10)  # ip entry
        button1 = tk.Button(self.RightPanel, text='Przejdź do gry', command=self.GoToCaptureCheckers, font=self.helv36)
        button1.grid(row=5, column=2, pady=5)

    def GoToCaptureCheckers(self):
        CaptureCheckersWindow(ip=self.CameraIP.get())
        self.OptionsWindow.destroy()

    def center(self):
        self.OptionsWindow.update_idletasks()
        width =  self.OptionsWindow.winfo_width()
        height =  self.OptionsWindow.winfo_height()
        x = ( self.OptionsWindow.winfo_screenwidth() // 2) - (width // 2)
        y = ( self.OptionsWindow.winfo_screenheight() // 2) - (height // 2)
        self.OptionsWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))