from PIL import Image, ImageTk
import tkinter as tk

from CaptureCheckersWindow import CaptureCheckersWindow
from BoardDetection import *


class OptionsClass:
    def __init__(self):
        self.vs = cv2.VideoCapture(0)
        self.current_image = None  # aktualny obraz z kamery
        self.CreateOptionWindow()

    def CreateOptionWindow(self):
        self.OptionsWindow = tk.Toplevel()  # inicjalizacja rooota
        self.OptionsWindow.title("Options")  # tytul okna
        self.OptionsWindow.protocol('WM_DELETE_WINDOW', self.destructor) # destrucor odpala się po zamknięciu okna
        self.CameraIPTextBox = tk.StringVar(self.OptionsWindow, value='http://192.168.137.70:4747/video%27')
        self.InitializePanels()
        self.InitializeCameraPanel()
        self.video_loop()

    def InitializeRightPanel(self):
        self.RightPanel = tk.Label(self.OptionsWindow)
        self.RightPanel.grid(row=0, column=1)
        self.InitializeRightPanelComponent()

    def InitializeRightPanelComponent(self):
        self.InitializeIpButton()
        self.InitializeIPEntry()
        self.InitializePlayButton()
        self.InitializeSliders()

    def InitializeSliders(self):
        frame_Slider = tk.Frame(self.RightPanel)
        frame_Slider.grid(row=1, column=2)

        tk.Label(self.RightPanel,text = 'Gracz 1' ).grid(row=1, column=1)
        tk.Label(frame_Slider, text='MIN').grid(row=0, column=0)
        tk.Label(frame_Slider, text='MAX').grid(row=0, column=2)

        tk.Scale(frame_Slider, from_=0, to=180, orient='horizontal').grid(row=0, column=1)
        tk.Scale(frame_Slider, from_=0, to=180, orient='horizontal').grid(row=0, column=3)



        frame_Slider2 = tk.Frame(self.RightPanel)
        frame_Slider2.grid(row=2, column=2)

        tk.Label(self.RightPanel,text = 'Gracz 2' ).grid(row=2, column=1)
        tk.Label(frame_Slider2, text='MIN').grid(row=0, column=0)
        tk.Label(frame_Slider2, text='MAX').grid(row=0, column=2)

        tk.Scale(frame_Slider2, from_=0, to=180, orient='horizontal').grid(row=0, column=1)
        tk.Scale(frame_Slider2, from_=0, to=180, orient='horizontal').grid(row=0, column=3)

    def InitializeIpButton(self):
        button1 = tk.Button(self.RightPanel, text='USTAW IP', command=self.InitializeCamera)
        button1.grid(row=0, column=1)  # pozycjonowanie

    def InitializeIPEntry(self):
        nentry = tk.Entry(self.RightPanel, width=50, textvariable=self.CameraIPTextBox).grid(row=0, column=2)

    def InitializePlayButton(self):
        button1 = tk.Button(self.RightPanel, text='Przejdź do GRY', command=self.GoToCaptureCheckers)
        button1.grid(row=5, column=2)

    def InitializePanels(self):
        self.InitializeRightPanel()
        self.InitializeCameraPanel()

    def InitializeCameraPanel(self):
        self.Camerapanel = tk.Label(self.OptionsWindow)  # inicjalizacja panelu z kamera
        self.Camerapanel.grid(row=0, column=0)  # pozycjonowanie panelu

    def GoToCaptureCheckers(self):
        #if self.vs.isOpened():
         #   CaptureCheckersWindow(vs=self.vs)
        #else:
         #   CaptureCheckersWindow(ip=self.CameraIPTextBox.get())

        CaptureCheckersWindow(ip ='http://192.168.137.69:4747/video%27')
        #self.OptionsWindow.destroy()


    def InitializeCamera(self):
        self.vs = cv2.VideoCapture(self.CameraIPTextBox.get()) # klatki z kamerki, 0 to domyślna

    def video_loop(self):
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA

            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.Camerapanel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.Camerapanel.config(image=imgtk)  # show the image

        self.OptionsWindow.after(30, self.video_loop)  # call the same function after 30 milliseconds

    def destructor(self):
        self.OptionsWindow.destroy()
        self.vs.release()
