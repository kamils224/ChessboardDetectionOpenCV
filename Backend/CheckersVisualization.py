from PIL import Image, ImageTk
import copy
import cv2


class Checkers_Board(): # klasa zajmująca się wizualizacją

    def __init__(self, image_board, visualisation, start_position):
        self.sprite = image_board # sprite - tło
        self.board = copy.deepcopy(self.sprite) # na tym jest rysowana jedna klatka
        self.Matrix = start_position
        self.visualisation = visualisation
        self.draw(start_position,1)

    def draw(self,PositionMatrix,flag):
        self.board = copy.deepcopy(self.sprite)
        for x in range(len(self.Matrix)):
            for y in range(len(self.Matrix[x])):
                if self.Matrix[y][x] != PositionMatrix[y][x] and flag:
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
                    cv2.circle(self.board, (50 + (x * 100), 50 + (y * 100)), 30, (223,5,255), -1)
                elif PositionMatrix[y][x] == 4:
                    cv2.circle(self.board, (50 + (x * 100), 50 + (y * 100)), 40, (0, 0, 255), -1)
                    cv2.circle(self.board, (50 + (x * 100), 50 + (y * 100)), 30, (3, 255, 255), -1)

        b, g, r = cv2.split(self.board)
        image = cv2.merge((r, g, b))
        image2 = Image.fromarray(image)
        tura8 = ImageTk.PhotoImage(image=image2)
        self.visualisation.configure(image=tura8)
        self.visualisation.image = tura8
        self.visualisation.grid(row= 0, column=1)
        self.Matrix = PositionMatrix


