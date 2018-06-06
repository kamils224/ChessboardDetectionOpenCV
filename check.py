
rows = 8
columns = 8
Matrix = [[0 for x in range(rows)] for y in range(columns)]

Matrix[0][0] = 1
Matrix[0][2] = 1
Matrix[0][4] = 1
Matrix[0][6] = 1

Matrix[1][1] = 0
Matrix[3][3] = 3
Matrix[1][3] = 1
Matrix[1][5] = 1
Matrix[1][7] = 1

Matrix[2][0] = 0
Matrix[3][1] = 1
Matrix[2][2] = 1
Matrix[2][4] = 1
Matrix[2][6] = 1

Matrix[5][1] = 0
Matrix[5][3] = 2
Matrix[4][0] = 2
Matrix[5][5] = 0
Matrix[4][4] = 2

Matrix[5][7] = 2

Matrix[6][0] = 2
Matrix[6][2] = 2
Matrix[6][4] = 2
Matrix[6][6] = 2

Matrix[7][1] = 2
Matrix[7][3] = 2
Matrix[7][5] = 2
Matrix[7][7] = 2



M2 = [[0 for x in range(rows)] for y in range(columns)]

M2[0][0] = 1
M2[0][2] = 1
M2[0][4] = 1
M2[0][6] = 1

M2[1][1] = 0
M2[3][3] = 3
M2[1][3] = 1
M2[1][5] = 1
M2[1][7] = 1

M2[2][0] = 1
M2[3][1] = 0
M2[2][2] = 1
M2[2][4] = 1
M2[2][6] = 1

M2[5][3] = 2
M2[4][0] = 2
M2[5][5] = 0
M2[4][4] = 2

M2[5][7] = 2

M2[6][0] = 2
M2[6][2] = 2
M2[6][4] = 2
M2[6][6] = 2

M2[7][1] = 2
M2[7][3] = 2
M2[7][5] = 2
M2[7][7] = 2


def explode(matrix):
    for i, row in enumerate(matrix):
        for j, int in enumerate(row):
            yield i, j, int

def NorthWest(i, j):
    return i-1, j-1


def NorthEast(i, j):
    return i-1, j+1


def SouthWest(i, j):
    return i+1, j-1


def SouthEast(i, j):
    return i+1, j+1


def NorthWest_jump(i, j):
    return i-2, j-2


def NorthEast_jump(i, j):
    return i-2, j+2


def SouthWest_jump(i, j):
    return i+2, j-2


def SouthEast_jump(i, j):
    return i+2, j+2


def player_change(p1, p2):
    if p1 == True:
        p1 = False
        p2 = True
    else:
        p1 = True
        p2 = False
    return p1, p2

def check_move(M1, M2, p1, p2):
    i_after = 9
    j_after = 9
    if M1 == M2:
        return print("Move not found")
    else:
        for i, j, int in explode(M1):
            if M1[i][j] != M2[i][j]:
                if int != 0:
                    i_before = i
                    j_before = j
                    if p1 and (M1[i_before][j_before] == 2 or M1[i_before][j_before] == 4):
                        return print("Nie twój pionek baranie! (Player_1) ")
                    if p2 and (M1[i_before][j_before] == 1 or M1[i_before][j_before] == 3):
                        return print("Nie twój pionek baranie! (Player_2) ")
                else:
                    i_after = i
                    j_after = j
        print("FROM: ", i_before, j_before)
        print("TO: ", i_after, j_after)

        if(i_after, j_after) == (9, 9):
            return print("OCCUPIED FIELD")
        else:
#DAME
            if M1[i_before][j_before] == 3 or M1[i_before][j_before] == 4:
                print("DAMKA")
                if i_after > i_before and j_after > j_before:
                    i_before = i_before + 1
                    j_before = j_before + 1
                    pawns_1 = 0
                    pawns_2 = 0
                    while i_before < i_after and j_before < j_after:
                        if M1[i_before][j_before] == 1 or M1[i_before][j_before] == 3:
                            pawns_1= pawns_1+1
                            i_op = i_before
                            j_op = j_before
                        if M1[i_before][j_before] == 2 or M1[i_before][j_before] == 4:
                            pawns_2= pawns_2+1
                            i_op=i_before
                            j_op=j_before
                        i_before = i_before + 1
                        j_before = j_before + 1
                    if p1 and pawns_1 == 0 and pawns_2 == 1:
                        print("SE direction")
                        return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                        # Player NOT change
                    elif p1 and pawns_1 == 0 and pawns_2 == 0:
                        print("SE direction")
                        return print("YES.Permission. Next Player")
                        # Player change
                    elif p2 and pawns_2 == 0 and pawns_1 == 1:
                        print("SE direction")
                        return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                        # Player NOT change
                    elif p2 and pawns_2 == 0 and pawns_1 == 0:
                        print("SE direction")
                        return print("YES.Permission. Next Player")
                        # Player change
                    else:
                        return print("Impossible movement (more pawns or own jumped)")
                if i_after > i_before and j_after < j_before:
                    i_before = i_before + 1
                    j_before = j_before - 1
                    pawns_1 = 0
                    pawns_2 = 0
                    while i_before < i_after and j_before > j_after:
                        if M1[i_before][j_before] == 1 or M1[i_before][j_before] == 3:
                            pawns_1 = pawns_1 + 1
                            i_op = i_before
                            j_op = j_before
                        if M1[i_before][j_before] == 2 or M1[i_before][j_before] == 4:
                            pawns_2 = pawns_2 + 1
                            i_op = i_before
                            j_op = j_before
                        i_before = i_before + 1
                        j_before = j_before - 1
                    if p1 and pawns_1 == 0 and pawns_2 == 1:
                        print("SW direction")
                        return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                        # Player NOT change
                    elif p1 and pawns_1 == 0 and pawns_2 == 0:
                        print("SW direction")
                        return print("YES.Permission. Next Player")
                        # Player change
                    elif p2 and pawns_2 == 0 and pawns_1 == 1:
                        print("SW direction")
                        return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                        # Player NOT change
                    elif p2 and pawns_2 == 0 and pawns_1 == 0:
                        print("SW direction")
                        return print("YES.Permission. Next Player")
                        # Player change
                    else:
                        return print("Impossible movement (more pawns or own jumped)")
                if i_after < i_before and j_after > j_before:
                    i_before = i_before - 1
                    j_before = j_before + 1
                    pawns_1 = 0
                    pawns_2 = 0
                    while i_before > i_after and j_before < j_after:
                        if M1[i_before][j_before] == 1 or M1[i_before][j_before] == 3:
                            pawns_1 = pawns_1 + 1
                            i_op = i_before
                            j_op = j_before
                        if M1[i_before][j_before] == 2 or M1[i_before][j_before] == 4:
                            pawns_2 = pawns_2 + 1
                            i_op = i_before
                            j_op = j_before
                        i_before = i_before - 1
                        j_before = j_before + 1
                    if p1 and pawns_1 == 0 and pawns_2 == 1:
                        print("NE direction")
                        return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                        # Player NOT change
                    elif p1 and pawns_1 == 0 and pawns_2 == 0:
                        print("NE direction")
                        return print("YES.Permission. Next Player")
                        # Player change
                    elif p2 and pawns_2 == 0 and pawns_1 == 1:
                        print("NE direction")
                        return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                        # Player NOT change
                    elif p2 and pawns_2 == 0 and pawns_1 == 0:
                        print("NE direction")
                        return print("YES.Permission. Next Player")
                        # Player change
                    else:
                        return print("Impossible movement (more pawns or own jumped)")
                if i_after < i_before and j_after < j_before:
                    i_before = i_before - 1
                    j_before = j_before - 1
                    pawns_1 = 0
                    pawns_2 = 0
                    while i_before > i_after and j_before > j_after:
                        if M1[i_before][j_before] == 1 or M1[i_before][j_before] == 3:
                            pawns_1 = pawns_1 + 1
                            i_op = i_before
                            j_op = j_before
                        if M1[i_before][j_before] == 2 or M1[i_before][j_before] == 4:
                            pawns_2 = pawns_2 + 1
                            i_op = i_before
                            j_op = j_before
                        i_before = i_before - 1
                        j_before = j_before - 1
                    if p1 and pawns_1 == 0 and pawns_2 == 1:
                        print("NW direction")
                        return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                        # Player NOT change
                    elif p1 and pawns_1 == 0 and pawns_2 == 0:
                        print("NW direction")
                        return print("YES.Permission. Next Player")
                        # Player change
                    elif p2 and pawns_2 == 0 and pawns_1 == 1:
                        print("NW direction")
                        return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                        # Player NOT change
                    elif p2 and pawns_2 == 0 and pawns_1 == 0:
                        print("NW direction")
                        return print("YES.Permission. Next Player")
                        # Player change
                    else:
                        return print("Impossible movement (more pawns or own jumped)")
#NORMAL
            else:
                if (i_after, j_after) == NorthWest(i_before, j_before):
                    print("NW direction")
                    if p1:
                        return print("YES.Permission. Next Player")
                        #Player change
                    else:
                        return print("CAN'T MOVE BACK!!!")
        #CHECK MOVE
                elif (i_after, j_after) == NorthEast(i_before, j_before):
                    print("NE direction")
                    if p1:
                        return print("YES.Permission. Next Player")
                        #Player change
                    else:
                        print("CAN'T MOVE BACK!!!")
                elif (i_after, j_after) == SouthWest(i_before, j_before):
                    print("SW direction")
                    if p2:
                        return print("YES.Permission. Next Player")
                        #Player change
                    else:
                       return print("CAN'T MOVE BACK!!!")
                elif (i_after, j_after) == SouthEast(i_before, j_before):
                    print("SE direction")
                    if p2:
                        return print("YES.Permission. Next Player")
                        #Player change
                    else:
                       return print("CAN'T MOVE BACK!!!")
        #CHECK JUMP
                elif (i_after, j_after) == NorthWest_jump(i_before, j_before):
                    print("NW_jump direction")
                    if p1:
                        (i_op, j_op) = NorthWest(i_before, j_before)
                        if M1[i_op][j_op] == 2 or M1[i_op][j_op] == 4:
                            return print("YES.Permission. Beaten pawn: ", i_op, j_op,"  Additional move")
                            #Player NOT change
                    elif p2:
                        (i_op, j_op) = NorthWest(i_before, j_before)
                        if M1[i_op][j_op] == 1 or M1[i_op][j_op] == 3:
                            return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                            # Player NOT change
                    else:
                        return print("Impossible movement (empty or own field jumped)")
                elif (i_after, j_after) == NorthEast_jump(i_before, j_before):
                    print("NE_jump direction")
                    if p1:
                        (i_op, j_op) = NorthEast(i_before, j_before)
                        if M1[i_op][j_op] == 2 or M1[i_op][j_op] == 4:
                            return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                            #Player NOT change
                    elif p2:
                        (i_op, j_op) = NorthEast(i_before, j_before)
                        if M1[i_op][j_op] == 1 or M1[i_op][j_op] == 3:
                            return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                            # Player NOT change
                    else:
                        return print("Impossible movement (empty or own field jumped)")
                elif (i_after, j_after) == SouthWest_jump(i_before, j_before):
                    print("SW_jump direction")
                    if p1:
                        (i_op, j_op) = SouthWest(i_before, j_before)
                        if M1[i_op][j_op] == 2 or M1[i_op][j_op] == 4:
                            return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                            #Player NOT change
                    elif p2:
                        (i_op, j_op) = SouthWest(i_before, j_before)
                        if M1[i_op][j_op] == 1 or M1[i_op][j_op] == 3:
                            return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                            # Player NOT change
                    else:
                        return print("Impossible movement (empty or own field jumped)")
                elif (i_after, j_after) == SouthEast_jump(i_before, j_before):
                    print("SE_jump direction")
                    if p1:
                        (i_op, j_op) = SouthEast(i_before, j_before)
                        if M1[i_op][j_op] == 2 or M1[i_op][j_op] == 4:
                            return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                            #Player NOT change
                    elif p2:
                        (i_op, j_op) = SouthEast(i_before, j_before)
                        if M1[i_op][j_op] == 1 or M1[i_op][j_op] == 3:
                            return print("YES.Permission. Beaten pawn: ", i_op, j_op, "  Additional move")
                            # Player NOT change
                    else:
                        return print("Impossible movement (empty or own field jumped)")
                else:
                    return print("Impossible movement (wrong color or too far)")

player_1 = True;
player_2 = False;
check_move(Matrix, M2, player_1, player_2)