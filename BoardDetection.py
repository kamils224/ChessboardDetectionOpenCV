import cv2
import numpy as np


class BoardDetection:
    video_device = 0
    width = 800
    height = 600

    def __init__(self, device=0, width=800, height=600):
        self.video_device = device
        self.width = width
        self.height = height

    def ConfigureBlobDetector(self):
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()

        params.filterByColor = True
        params.blobColor = 0

        # Change thresholds
        params.minThreshold = 10;
        params.maxThreshold = 200;

        # Filter by Area.
        params.filterByArea = False
        params.minArea = 100

        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.1

        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = 0.87

        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.01

        return cv2.SimpleBlobDetector_create(params)

    def Detect(self):

        cap = cv2.VideoCapture(self.video_device)
        detector = self.ConfigureBlobDetector()

        # kernel to dilate and erode
        small_kernel = np.ones((5, 5), np.uint8)
        big_kernel = np.ones((20, 20), np.uint8)

        while True:

            ret, frame = cap.read()
            img = cv2.resize(frame, (self.width, self.height))

            # HSV conversion
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # sensitivity of color detection
            sensitivity_high = 25
            sensitivity_small = 15
            mask = cv2.inRange(hsv, (60 - sensitivity_high, 100 - sensitivity_small, 100 - sensitivity_small),
                               (60 + sensitivity_high, 255, 255))

            # creating binary image with markers
            mask_erode = cv2.erode(mask, small_kernel, iterations=2)
            mask_dilate = cv2.dilate(mask_erode, big_kernel)
            # blob detection does not detect white color, image must be inverted
            inverted_mask = cv2.bitwise_not(mask_dilate)

            keypoints = detector.detect(inverted_mask)
            im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255),
                                                  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            markers_position = []

            # correct image has 4 markers
            if len(keypoints) == 4:
                for i in keypoints:
                    # print(str(i.pt[0])+' - '+str(i.pt[1]))
                    x_pos = np.around(i.pt[0])
                    y_pos = np.around(i.pt[1])
                    markers_position.append((x_pos, y_pos))

                markers_position = sorted(markers_position, key=lambda k: [k[0], k[1]])
                # print(markers_position)

                pts1 = np.float32([markers_position[1], markers_position[2], markers_position[0], markers_position[3]])

                pts2 = np.float32([[0, 0], [self.width, 0], [0, self.height], [self.width, self.height]])

                # perspective transform to extract board
                M = cv2.getPerspectiveTransform(pts1, pts2)
                warp = cv2.warpPerspective(img, M, (self.width, self.height))
                # offset to cut edges of the board
                vertical_offset = 10
                horizontal_offset = 20
                board = warp[vertical_offset:self.height - vertical_offset,
                        horizontal_offset:self.width - horizontal_offset]

                board_hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
                # size of the board
                boardHeight, boardWidth, boardChannels = board.shape
                # size of the one block
                blockHeight = int(boardHeight / 8)
                blockWidth = int(boardWidth / 8)

                board_blocks = []
                for i in range(0, 8):
                    for j in range(0, 8):
                        board_blocks.append(
                            board[i * blockHeight:i * blockHeight + blockHeight,
                            j * blockWidth:j * blockWidth + blockWidth])

                #print('average_color')
                final_list = []
                for b in board_blocks:
                    b_cvt = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
                    average_color = cv2.mean(b_cvt)

                    if 130 < average_color[0] < 150:
                        # print('red')
                        final_list.append(1)
                    elif 90 < average_color[0] < 105:
                        # print('blue')
                        final_list.append(2)
                    else:
                        # print('blank')
                        final_list.append(0)

                # todo - fix pawn detection
                # wyswietlenie planszy
                cv2.imshow('board', board)
                mask_blue = cv2.inRange(board_hsv, (90, 80, 80), (130, 255, 255))
                mask_blue = cv2.erode(mask_blue, small_kernel, iterations=4)
                mask_blue = cv2.dilate(mask_blue, small_kernel, iterations=1)

                mask_red = cv2.inRange(board_hsv, (150, 80, 80), (179, 255, 255))
                # mask_red = cv2.erode(mask_red,bigKernel,iterations=1)
                mask_red = cv2.dilate(mask_red, big_kernel, iterations=1)
                mask_red = cv2.erode(mask_red, big_kernel, iterations=1)

                cv2.imshow('blue', mask_blue)
                cv2.imshow('red', mask_red)

                print(final_list)

            # cv2.imshow('main', img)
            # cv2.imshow('mask', inverted_mask)
            cv2.imshow('keypoints', im_with_keypoints)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
