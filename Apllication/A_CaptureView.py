from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox
from Backend.CheckersVisualization import Checkers_Board
from Backend.BoardDetection import BoardDetection
from Backend.LoadedGameManager import *
import cv2
import threading
from Backend.correct_moves import check_move

from tkinter import *


class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def createToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


class CaptureCheckersWindow:
    StartingMatrix = [[1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 2, 0, 2, 0, 2],
                      [2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2]]
    MatrixBefore = [[0 for x in range(8)] for y in range(8)]

    player1 = False
    player2 = True
    round = 1
    gameHistory=[]

    def __init__(self, ip=0):
        self.detection = BoardDetection()
        self.detection.video_device = ip
        self.root = tk.Toplevel()  # inicjalizacja rooota
        self.root.title("Checkers")  # tytul okna
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)  # destrucor odpala się po zamknięciu okna

        for x in range(0, 8):
            for y in range(0, 8):
                self.MatrixBefore[x][y] = 0

        self.Checkers_panel = tk.Label(self.root)
        self.Checkers_panel.grid(row=0, column=0)

        self.UserFrame = tk.Frame(self.root)
        self.UserFrame.grid(row=1, column=1)

        self.panel2 = tk.Label(self.UserFrame)
        self.panel2.pack(side="bottom", fill="both", expand=1)

        self.DeafaultBoard()

        self.video_loop()

    def DeafaultBoard(self):
        self.Initialize()
        boardImage = cv2.imread('Image/szachownica.png')  # wczytanie szablonu , tła do warcab
        Matrix888 = [[0 for x in range(8)] for y in range(8)]
        self.board_game = Checkers_Board(boardImage, self.Checkers_panel, Matrix888)

    def Initialize(self):
        helv36 = tkfont.Font(family='Helvetica', size=15, weight='bold')

        MoveButton = tk.Button(self.panel2, text="Wykonaj Ruch", command=self.Catch,
                               font=helv36)
        MoveButton.pack(side="right", fill="both", expand=1)

        SaveButton = tk.Button(self.panel2, text="Zapisz grę", command=self.SaveGame(),
                               font=helv36)
        SaveButton.pack(side="right", fill="both", expand=1)

        NewGameButton = tk.Button(self.panel2, text="Nowa gra", command=self.StartGame,
                                  font=helv36)
        NewGameButton.pack(side="left", fill="both", expand=1)

        ResetPawnsButton = tk.Button(self.panel2, text="Resetuj pozycje", command=self.SetPawns,
                                     font=helv36)
        ResetPawnsButton.pack(side="left", fill="both", expand=1)

        createToolTip(MoveButton, "Pobiera aktualną pozycję pionków i sprawdza poprawność ruchu")
        createToolTip(NewGameButton, "Pobiera pozycję pionków i sprawdza czy ustawienie jest zgodne z początkiem gry")
        createToolTip(ResetPawnsButton,
                      "Aktualizacja pozycji pionków bez sprawdzenia poprawności ruchu, używać tylko w przypadku błędów")

        self.InfoLabel = tk.Label(self.panel2, text="Rozpocznij nową grę")
        self.InfoLabel.pack(side="bottom", fill="both", expand=1)
        self.InfoLabel.config(width=25, font=("Courier", 30))

        self.CurrentPlayerLabel = tk.Label(self.panel2, text="Brak pionków")
        self.CurrentPlayerLabel.pack(side="bottom", fill="both", expand=1)
        self.CurrentPlayerLabel.config(width=25, font=("Courier", 30))

    def Catch(self):

        board = self.detection.result_list
        print(board)
        MatrixDraw = [[0 for x in range(8)] for y in range(8)]
        i = 0
        for x in range(0, 8):
            for y in range(0, 8):
                MatrixDraw[x][y] = board[i]
                i += 1

        print(self.MatrixBefore)
        print(MatrixDraw)
        # sprawdzenie poprawności ruchu
        correct = check_move(self.MatrixBefore, MatrixDraw, self.player1, self.player2)

        # jeżeli ruch był poprawny zaktualizuj macierz
        if correct is None:
            pass
        elif correct[0]:
            # dodanie ruchu do historii rozgrywki
            self.gameHistory.append(MatrixDraw)
            # rysowanie planszy
            self.board_game.draw(MatrixDraw, 0)
            self.MatrixBefore = MatrixDraw
            self.player1 = not self.player1
            self.player2 = not self.player2
            self.ChangePlayerLabel()
            self.round += 1
            self.InfoLabel.config(text='Tura' + str(self.round))

        else:
            messagebox.showinfo('Błąd', correct[1] + '\nCofnij pionek na właściwe miejsce')

    def StartGame(self):

        result = messagebox.askokcancel('Nowa gra', 'Czy na pewno chcesz rozpocząć nową grę?')

        if result is True:
            self.gameHistory.clear()
            board = self.detection.result_list
            MatrixDraw = [[0 for x in range(8)] for y in range(8)]
            i = 0
            for x in range(0, 8):
                for y in range(0, 8):
                    MatrixDraw[x][y] = board[i]
                    i += 1

            if (self.CompareBoards(MatrixDraw,self.StartingMatrix)):
                self.board_game.draw(MatrixDraw, 0)
                self.ChangePlayerLabel()
                self.InfoLabel.config(text='Tura' + str(self.round))
                self.MatrixBefore=MatrixDraw
            else:
                messagebox.showinfo('Błąd','Niepoprawne ustawienie pionków')

        else:
            pass

    def SetPawns(self):
        board = self.detection.result_list
        MatrixDraw = [[0 for x in range(8)] for y in range(8)]
        i = 0
        for x in range(0, 8):
            for y in range(0, 8):
                MatrixDraw[x][y] = board[i]
                i += 1
        self.MatrixBefore = MatrixDraw
        self.board_game.draw(MatrixDraw, 0)

    def ChangePlayerLabel(self):
        if self.player1:
            self.CurrentPlayerLabel.config(text='Tura gracza niebieskiego')
        else:
            self.CurrentPlayerLabel.config(text='Tura gracza czerwonego')

    def video_loop(self):
        t = threading.Thread(target=self.detection.StartDetection)
        t.start()

    def destructor(self):
        self.root.destroy()

    def CompareBoards(self, M1, M2):
        for x in range(0, 8):
            for y in range(0, 8):
                if M1[x][y] == M2[x][y]:
                    continue
                else:
                    return False
        return True

    def SaveGame(self):
        pass