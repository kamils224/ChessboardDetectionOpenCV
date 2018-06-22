import cv2
import numpy as np


class BoardDetection:


    video_device = 0
    width = 800
    height = 600

    markers_color_detection_sensitivity = 15
    markers_color_detection_sensitivity2 = 15

    # offset after markers detection
    horizontalOffset = 20
    verticalOffset = 10

    # the size of one block
    blockWidth = ((width - horizontalOffset) / 8)
    blockHeight = ((height - verticalOffset) / 8)

    green_offset=0
    blue_offset=0
    red_offset=0
    purple_offset=0
    yellow_offset=0


    print(blockWidth)
    print(blockHeight)

    board_blocks = []

    button_clicked = False

    def __init__(self, device=0, width=800, height=600):
        self.result_list = np.zeros(64, dtype=int)
        self.video_device = device
        self.width = width
        self.height = height
        for y in range(0, 8):
            for x in range(0, 8):
                self.board_blocks.append(((x * self.blockWidth, (x + 1) * self.blockWidth),
                                          (y * self.blockHeight, (y + 1) * self.blockHeight)))

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


    def CheckPawnLocation(self, board=[], x=0, y=0):
        for item in board:
            if item[0][0] <= x < item[0][1] and item[1][0] <= y < item[1][1]:
                return self.board_blocks.index(item)
        return None

    def Detect(self,frame=None, detector = None):

        img = cv2.resize(frame, (self.width, self.height))

        # HSV conversion
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, (60 - self.markers_color_detection_sensitivity,
                                 100 - self.markers_color_detection_sensitivity2,
                                 100 - self.markers_color_detection_sensitivity2),
                           (60 + self.markers_color_detection_sensitivity, 255, 255))

        smallKernel = np.ones((5, 5), np.uint8)
        bigKernel = np.ones((20, 20), np.uint8)
        mask_erode = cv2.erode(mask, smallKernel, iterations=2)
        mask_dilate = cv2.dilate(mask_erode, bigKernel)
        inverted_mask = cv2.bitwise_not(mask_dilate)

        keypoints = detector.detect(inverted_mask)
        im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        markers_position = []

        if len(keypoints) == 4:
            for i in keypoints:
                # uncomment to check marker position
                # print(str(i.pt[0])+' - '+str(i.pt[1]))

                x_pos = np.around(i.pt[0])
                y_pos = np.around(i.pt[1])
                markers_position.append((x_pos, y_pos))

            markers_position = sorted(markers_position, key=lambda k: [k[0], k[1]])

            # uncomment to check marker's properties
            # print(markers_position)

            pts1 = np.float32([markers_position[1], markers_position[2], markers_position[0], markers_position[3]])

            pts2 = np.float32([[0, 0], [self.width, 0], [0, self.height], [self.width, self.height]])

            # perspective transform
            M = cv2.getPerspectiveTransform(pts1, pts2)
            warp = cv2.warpPerspective(img, M, (self.width, self.height))

            board = warp[self.verticalOffset:self.height - self.verticalOffset,
                    self.horizontalOffset:self.width - self.horizontalOffset]
            board_hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)

            # show board
            # cv2.imshow('board', board)

            # BLUE mask
            mask_blue = cv2.inRange(board_hsv, (90, 80, 80), (110, 255, 255))
            mask_blue = cv2.erode(mask_blue, smallKernel, iterations=2)
            mask_blue = cv2.dilate(mask_blue, smallKernel, iterations=2)
            inverted_mask_blue = cv2.bitwise_not(mask_blue)

            # RED mask
            mask_red1 = cv2.inRange(board_hsv, (0, 80, 80), (10, 255, 255))
            mask_red2 = cv2.inRange(board_hsv, (170, 80, 80), (180, 255, 255))
            mask_red = cv2.bitwise_or(mask_red1, mask_red2)
            mask_red = cv2.erode(mask_red, smallKernel, iterations=2)
            mask_red = cv2.dilate(mask_red, smallKernel, iterations=2)
            inverted_mask_red = cv2.bitwise_not(mask_red)

            # PURPLE MASK
            mask_purple = cv2.inRange(board_hsv, (110, 80, 80), (130, 255, 255))
            mask_purple = cv2.erode(mask_purple, smallKernel, iterations=2)
            mask_purple = cv2.dilate(mask_purple, smallKernel, iterations=2)
            inverted_mask_purple = cv2.bitwise_not(mask_purple)

            # YELLOW MASK
            mask_yellow = cv2.inRange(board_hsv, (20, 80, 80), (40, 255, 255))
            mask_yellow = cv2.erode(mask_yellow, smallKernel, iterations=2)
            mask_yellow = cv2.dilate(mask_yellow, smallKernel, iterations=2)
            inverted_mask_yellow = cv2.bitwise_not(mask_yellow)

            # Find blobs
            blue_keypoints = detector.detect(inverted_mask_blue)
            red_keypoints = detector.detect(inverted_mask_red)
            purple_keypoints = detector.detect(inverted_mask_purple)
            yellow_keypoints = detector.detect(inverted_mask_yellow)

            # draw detected keypoints
            board = cv2.drawKeypoints(board, blue_keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            board = cv2.drawKeypoints(board, purple_keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            board = cv2.drawKeypoints(board, red_keypoints, np.array([]), (255, 0, 0),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            board = cv2.drawKeypoints(board, yellow_keypoints, np.array([]), (255, 0, 0),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)



            if (True):

                #result_list = np.zeros(64, dtype=int)

                for point in blue_keypoints:
                    x = point.pt[0]
                    y = point.pt[1]
                    index = self.CheckPawnLocation(self.board_blocks, x, y)
                    if (index is not None):
                        self.result_list[index] = 1

                for point in purple_keypoints:
                    x = point.pt[0]
                    y = point.pt[1]
                    index = self.CheckPawnLocation(self.board_blocks, x, y)
                    if (index is not None):
                        self.result_list[index] = 3

                for point in red_keypoints:
                    x = point.pt[0]
                    y = point.pt[1]
                    index = self.CheckPawnLocation(self.board_blocks, x, y)
                    if (index is not None):
                        self.result_list[index] = 2

                for point in yellow_keypoints:
                    x = point.pt[0]
                    y = point.pt[1]
                    index = self.CheckPawnLocation(self.board_blocks, x, y)
                    if (index is not None):
                        self.result_list[index] = 4
                self.button_clicked=False
                return board


    def StartDetection(self):
        detector = self.ConfigureBlobDetector()
        cap = cv2.VideoCapture(self.video_device)


        while True:

            ret, frame = cap.read()
            img = cv2.resize(frame, (self.width, self.height))

            # HSV conversion
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv, (60 - self.markers_color_detection_sensitivity,
                                     100 - self.markers_color_detection_sensitivity2,
                                     100 - self.markers_color_detection_sensitivity2),
                               (60 + self.markers_color_detection_sensitivity, 255, 255))

            smallKernel = np.ones((5, 5), np.uint8)
            bigKernel = np.ones((20, 20), np.uint8)
            mask_erode = cv2.erode(mask, smallKernel, iterations=2)
            mask_dilate = cv2.dilate(mask_erode, bigKernel)
            inverted_mask = cv2.bitwise_not(mask_dilate)

            keypoints = detector.detect(inverted_mask)
            im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255),
                                                  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            markers_position = []

            if len(keypoints) == 4:
                for i in keypoints:
                    # uncomment to check marker position
                    # print(str(i.pt[0])+' - '+str(i.pt[1]))

                    x_pos = np.around(i.pt[0])
                    y_pos = np.around(i.pt[1])
                    markers_position.append((x_pos, y_pos))

                markers_position = sorted(markers_position, key=lambda k: [k[0], k[1]])

                # uncomment to check marker's properties
                # print(markers_position)

                pts1 = np.float32([markers_position[1], markers_position[2], markers_position[0], markers_position[3]])

                pts2 = np.float32([[0, 0], [self.width, 0], [0, self.height], [self.width, self.height]])

                # perspective transform
                M = cv2.getPerspectiveTransform(pts1, pts2)
                warp = cv2.warpPerspective(img, M, (self.width, self.height))

                board = warp[self.verticalOffset:self.height - self.verticalOffset,
                        self.horizontalOffset:self.width - self.horizontalOffset]
                board_hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)

                # show board
                # cv2.imshow('board', board)

                #BLUE mask
                mask_blue = cv2.inRange(board_hsv, (90, 80, 80), (110, 255, 255))
                mask_blue = cv2.erode(mask_blue, smallKernel, iterations=2)
                mask_blue = cv2.dilate(mask_blue, smallKernel, iterations=2)
                inverted_mask_blue = cv2.bitwise_not(mask_blue)

                #RED mask
                mask_red1 = cv2.inRange(board_hsv, (0, 80, 80), (10, 255, 255))
                mask_red2 = cv2.inRange(board_hsv, (170, 80, 80), (180, 255, 255))
                mask_red = cv2.bitwise_or(mask_red1, mask_red2)
                mask_red = cv2.erode(mask_red, smallKernel, iterations=2)
                mask_red = cv2.dilate(mask_red, smallKernel, iterations=2)
                inverted_mask_red = cv2.bitwise_not(mask_red)

                #PURPLE MASK
                mask_purple = cv2.inRange(board_hsv, (110, 80, 80), (130, 255, 255))
                mask_purple = cv2.erode(mask_purple, smallKernel, iterations=2)
                mask_purple = cv2.dilate(mask_purple, smallKernel, iterations=2)
                inverted_mask_purple = cv2.bitwise_not(mask_purple)

                #YELLOW MASK
                mask_yellow = cv2.inRange(board_hsv, (20, 80, 80), (40, 255, 255))
                mask_yellow = cv2.erode(mask_yellow, smallKernel, iterations=2)
                mask_yellow = cv2.dilate(mask_yellow, smallKernel, iterations=2)
                inverted_mask_yellow = cv2.bitwise_not(mask_yellow)

                #Find blobs
                blue_keypoints = detector.detect(inverted_mask_blue)
                red_keypoints = detector.detect(inverted_mask_red)
                purple_keypoints = detector.detect(inverted_mask_purple)
                yellow_keypoints = detector.detect(inverted_mask_yellow)


                #draw detected keypoints
                board = cv2.drawKeypoints(board, blue_keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                board = cv2.drawKeypoints(board, purple_keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                board = cv2.drawKeypoints(board, red_keypoints, np.array([]), (255, 0, 0),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                board = cv2.drawKeypoints(board, yellow_keypoints, np.array([]), (255, 0, 0),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                cv2.imshow('Pawns', board)

                if (True):

                    result_list = np.zeros(64, dtype=int)

                    for point in blue_keypoints:
                        x = point.pt[0]
                        y = point.pt[1]
                        index = self.CheckPawnLocation(self.board_blocks, x, y)
                        if (index is not None):
                            result_list[index] = 1

                    for point in purple_keypoints:
                        x = point.pt[0]
                        y = point.pt[1]
                        index = self.CheckPawnLocation(self.board_blocks, x, y)
                        if (index is not None):
                            result_list[index] = 3

                    for point in red_keypoints:
                        x = point.pt[0]
                        y = point.pt[1]
                        index = self.CheckPawnLocation(self.board_blocks, x, y)
                        if (index is not None):
                            result_list[index] = 2

                    for point in yellow_keypoints:
                        x = point.pt[0]
                        y = point.pt[1]
                        index = self.CheckPawnLocation(self.board_blocks, x, y)
                        if (index is not None):
                            result_list[index] = 4

                    button_clicked = False


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture

        cap.release()
        cv2.destroyAllWindows()


