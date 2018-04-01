import cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import *
from PIL import Image, ImageTk

rows = 8
columns = 8

Matrix = [[0 for x in range(rows)] for y in range(columns)]

Matrix[0][0] = 1
Matrix[0][2] = 1
Matrix[0][4] = 1
Matrix[0][6] = 1

Matrix[1][1] = 1
Matrix[1][3] = 1
Matrix[1][5] = 1
Matrix[1][7] = 1

Matrix[2][0] = 1
Matrix[2][2] = 1
Matrix[2][4] = 1
Matrix[2][6] = 1

Matrix[5][1] = 3
Matrix[5][3] = 3
Matrix[5][5] = 4
Matrix[5][7] = 4

Matrix[6][0] = 2
Matrix[6][2] = 2
Matrix[6][4] = 2
Matrix[6][6] = 2

Matrix[7][1] = 2
Matrix[7][3] = 2
Matrix[7][5] = 2
Matrix[7][7] = 2


image = cv2.imread('szachownica.png')


for x in range(rows):
    for y in range(columns):
        if Matrix[y][x] == 1:
            cv2.circle(image, (50 + (x * 100), 50 + (y * 100)), 40, (200,113,19), -1)
        elif Matrix[y][x] == 2:
            cv2.circle(image, (50 + (x * 100), 50 + (y * 100)), 40, (0, 0, 255), -1)
        elif Matrix[y][x] == 3:
            cv2.circle(image, (50 + (x * 100), 50 + (y * 100)), 40, (200,113,19), -1)
            cv2.circle(image, (50 + (x * 100), 50 + (y * 100)), 30, (150,113,19), -1)
        elif Matrix[y][x] == 4:
            cv2.circle(image, (50 + (x * 100), 50 + (y * 100)), 40, (0, 0, 100), -1)
            cv2.circle(image, (50 + (x * 100), 50 + (y * 100)), 30, (0, 0, 255), -1)


def close():
    exit()

window = Tk()

b,g,r = cv2.split(image)
img = cv2.merge((r,g,b))

im = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=im)

Label(window, image=imgtk).pack()

menubar = Menu(window)



filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="close",command=close)

menubar.add_cascade(label = "File", menu=filemenu)

window.config(menu=menubar)

window.mainloop()






cv2.waitKey(0)

