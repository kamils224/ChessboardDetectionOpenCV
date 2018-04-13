import cv2
import numpy as np

def DetectBoard():
    # rozdzielczość testowa, myślę że oficjalnie będzie wyższa
    width = 800
    height = 600

    img_input = cv2.imread('Image/plansza_marker_pionki.png')
    img = cv2.resize(img_input, (width, height))
    # konwersja na HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # czułość wykrywania kolorów, większa wartość to większy zakres barw
    sensitivity = 15
    mask_green = cv2.inRange(hsv, (60 - sensitivity, 100, 100), (60 + sensitivity, 255, 255))
    mask_yellow = cv2.inRange(hsv, (25 - sensitivity, 100, 100), (25 + sensitivity, 255, 255))
    # połączenie masek obu kolorów
    mask = cv2.bitwise_or(mask_green, mask_yellow)
    # kontury
    img2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # momenty, czyli okreslenie punktów centralnych konturów
    M0 = cv2.moments(contours[3])
    M1 = cv2.moments(contours[1])
    M2 = cv2.moments(contours[2])
    M3 = cv2.moments(contours[0])

    pts1 = np.float32(
        [[int(M0['m10'] / M0['m00']), int(M0['m01'] / M0['m00'])],
         [int(M2['m10'] / M2['m00']), (M2['m01'] / M2['m00'])],
         [int(M3['m10'] / M3['m00']), (M3['m01'] / M3['m00'])], [int(M1['m10'] / M1['m00']), (M1['m01'] / M1['m00'])]])

    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # ustawienie perspektywy na planszę
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warp = cv2.warpPerspective(img, M, (width, height))

    # wycięcie brzegów niebędących planszą
    verticalOffset = 27
    horizontalOffset = 43
    board = warp[verticalOffset:height - verticalOffset, horizontalOffset:width - horizontalOffset]

    # ustalenie docelowych wymiarów planszy
    boardHeight, boardWidth, boardChannels = board.shape
    # rozmiar pojedynczego bloku
    stepH = int(boardHeight / 8)
    stepW = int(boardWidth / 8)

    board_blocks = []

    for i in range(0, 8):
        for j in range(0, 8):
            board_blocks.append(board[i * stepH:i * stepH + stepH, j * stepW:j * stepW + stepW])

    # cv2.drawContours(img, contours, -1, (255, 0, 0), 2)

    # cv2.imshow('Main', img)
    # cv2.imshow('Mask', mask)
    # cv2.imshow('Warp', warp)
    # cv2.imshow('Board', board)

    # kolejnosc wypelniania listy, najpierw rzędami, od góry do dołu
    finalList = []

    for b in board_blocks:
        b_cvt = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
        h, w, c = b.shape
        color = b_cvt[int(h / 2), int(w / 2)]
        if 170 < color[0] < 190:
            #print('red')
            finalList.append(1)
        elif 90 < color[0] < 110:
            #print('blue')
            finalList.append(2)
        else:
            #print('blank')
            finalList.append(0)

    return finalList