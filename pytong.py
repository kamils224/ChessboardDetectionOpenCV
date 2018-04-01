import copy

from PIL import Image, ImageTk
import tkinter as tk
import argparse
import cv2



nowyruch = [[0 for x in range(8)] for y in range(8)]
nowyruch[0][0] = 1
nowyruch[0][2] = 1
nowyruch[0][4] = 1
nowyruch[0][6] = 1

nowyruch[1][1] = 1
nowyruch[1][3] = 1
nowyruch[1][5] = 1
nowyruch[1][7] = 1

nowyruch[3][1] = 1
nowyruch[2][2] = 1
nowyruch[2][4] = 1
nowyruch[2][6] = 1

nowyruch[5][1] = 2
nowyruch[5][3] = 2
nowyruch[5][5] = 2
nowyruch[5][7] = 2

nowyruch[6][0] = 2
nowyruch[6][2] = 2
nowyruch[6][4] = 2
nowyruch[6][6] = 2

nowyruch[7][1] = 2
nowyruch[7][3] = 2
nowyruch[7][5] = 2
nowyruch[7][7] = 2

class Checkers_Board():

    def __init__(self, row, columns, image_board):
        self.rows = row
        self.columns = columns
        self.sprite = image_board
        self.board = copy.deepcopy(self.sprite)
        self.Matrix = [[0 for x in range(self.rows)] for y in range(self.columns)]
        self.start_standard()

    def start_standard(self):
        self.Matrix[0][0] = 1
        self.Matrix[0][2] = 1
        self.Matrix[0][4] = 1
        self.Matrix[0][6] = 1

        self.Matrix[1][1] = 1
        self.Matrix[1][3] = 1
        self.Matrix[1][5] = 1
        self.Matrix[1][7] = 1

        self.Matrix[2][0] = 1
        self.Matrix[2][2] = 1
        self.Matrix[2][4] = 1
        self.Matrix[2][6] = 1

        self.Matrix[5][1] = 2
        self.Matrix[5][3] = 2
        self.Matrix[5][5] = 2
        self.Matrix[5][7] = 2

        self.Matrix[6][0] = 2
        self.Matrix[6][2] = 2
        self.Matrix[6][4] = 2
        self.Matrix[6][6] = 2

        self.Matrix[7][1] = 2
        self.Matrix[7][3] = 2
        self.Matrix[7][5] = 2
        self.Matrix[7][7] = 2

        self.draw(self.Matrix)

    def start_position(self,PositionMatrix):
        self.Matrix = PositionMatrix

    def draw(self,PositionMatrix):
        self.board = copy.deepcopy(self.sprite)
        for x in range(self.rows):
            for y in range(self.columns):
                if self.Matrix[y][x]!= PositionMatrix[y][x]:
                    cv2.rectangle(self.board, (2+(x * 100), 2+(y * 100)), (98+(x * 100), 98+(y * 100)), (0, 255, 0), 4)
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

    def return_board(self):
        image9 = self.board
        b, g, r = cv2.split(image9)
        img98 = cv2.merge((r, g, b))
        im98 = Image.fromarray(img98)
        imgtk98 = ImageTk.PhotoImage(image=im98)
        return imgtk98

    def __del__(self):
        print ('deleting Chceckers_board:  ', id(self))

class Application:
    def __init__(self, output_path = "./"):
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
        self.vs = cv2.VideoCapture(0) # capture video frames, 0 is your default video camera
        self.output_path = output_path  # store output path
        self.current_image = None  # current image from the camera

        self.root = tk.Tk()  # initialize root window
        self.root.title("PyImageSearch PhotoBooth")  # set window title
        # self.destructor function gets fired when the window is closed
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)

        self.panel = tk.Label(self.root)  # initialize image panel
        self.panel.pack(side="left", padx=10, pady=10)

        image9 = cv2.imread('szachownica.png')

        self.board_game = Checkers_Board(8, 8, image9)

        next_image = self.board_game.return_board()
        self.panelB = tk.Label(self.root, image=next_image)
        self.panelB.image = next_image
        self.panelB.pack(side="right", padx=0, pady=0)


        # create a button, that when pressed, will take the current frame and save it to file
        btn = tk.Button(self.root, text="move forward", command=self.move_forward)
        btn.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        btn = tk.Button(self.root, text="move backward", command=self.move_backward)
        btn.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        # start a self.video_loop that constantly pools the video sensor
        # for the most recently read frame
        self.video_loop()

    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image
        self.root.after(30, self.video_loop)  # call the same function after 30 milliseconds

    def move_forward(self):
        self.board_game.draw(nowyruch)
        wynik = self.board_game.return_board()
        self.panelB.configure(image=wynik)
        self.panelB.image = wynik

        print("[INFO] next move {}")

    def move_backward(self):
        print("[INFO] next move {}")

    def destructor(self):
        """ Destroy the root object and release all resources """
        print("[INFO] closing...")
        self.root.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="./",
    help="path to output directory to store snapshots (default: current folder")
args = vars(ap.parse_args())

# start the app
print("[INFO] starting...")
pba = Application(args["output"])
pba.root.mainloop()