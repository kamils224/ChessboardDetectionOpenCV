from PIL import Image, ImageTk
import tkinter as tk

from Apllication.A_CaptureView import CaptureCheckersWindow
from Backend.BoardDetection import *


class OptionsClass:
    def __init__(self):
        self.CreateOptionWindow()

    def CreateOptionWindow(self):
        self.OptionsWindow = tk.Toplevel()  # inicjalizacja rooota
        self.OptionsWindow.title("Options")  # tytul okna
        self.OptionsWindow.protocol('WM_DELETE_WINDOW', self.destructor) # destrucor odpala się po zamknięciu okna
        self.CameraIP = tk.StringVar(self.OptionsWindow, value='http://192.168.137.70:4747/video%27')
        self.InitializePanels()
        self.center()

    def InitializeRightPanel(self):
        self.RightPanel = tk.Label(self.OptionsWindow)
        self.RightPanel.grid(row=0, column=1)
        self.InitializeRightPanelComponent()

    def InitializeRightPanelComponent(self):
        tk.Entry(self.RightPanel, width=50, textvariable=self.CameraIP).grid(row=0, column=2) #ip entry
        self.InitializePlayButton()

    def InitializePlayButton(self):
        button1 = tk.Button(self.RightPanel, text='Przejdź do GRY', command=self.GoToCaptureCheckers)
        button1.grid(row=5, column=2)

    def InitializePanels(self):
        self.InitializeRightPanel()

    def GoToCaptureCheckers(self):
        CaptureCheckersWindow(ip=self.CameraIP.get())
        self.OptionsWindow.destroy()

    def destructor(self):
        self.OptionsWindow.destroy()

    def center(self):
        self.OptionsWindow.update_idletasks()
        width =  self.OptionsWindow.winfo_width()
        height =  self.OptionsWindow.winfo_height()
        x = ( self.OptionsWindow.winfo_screenwidth() // 2) - (width // 2)
        y = ( self.OptionsWindow.winfo_screenheight() // 2) - (height // 2)
        self.OptionsWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))