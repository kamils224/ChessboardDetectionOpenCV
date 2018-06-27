import copy


# rows = 8
# columns = 8
# #Matrix_before plansza przed wykonaniem ruchu
# Matrix_before = [[0 for x in range(rows)] for y in range(columns)]
#
# Matrix_before[0][1] = 1
# Matrix_before[0][3] = 1
# Matrix_before[0][5] = 1
# Matrix_before[0][7] = 1
#
# Matrix_before[1][0] = 0
# Matrix_before[1][2] = 1
# Matrix_before[1][4] = 1
# Matrix_before[1][6] = 1
#
# Matrix_before[2][1] = 1
# Matrix_before[2][3] = 0
# Matrix_before[2][5] = 1
# Matrix_before[2][7] = 3
#
# Matrix_before[3][0] = 0
# Matrix_before[3][2] = 0
# Matrix_before[3][4] = 2
# Matrix_before[3][6] = 2
#
# Matrix_before[4][1] = 2
# Matrix_before[4][3] = 0
# Matrix_before[4][5] = 0
# Matrix_before[4][7] = 0
#
# Matrix_before[5][0] = 1
# Matrix_before[5][2] = 0
# Matrix_before[5][4] = 2
# Matrix_before[5][6] = 2
#
# Matrix_before[6][1] = 0
# Matrix_before[6][3] = 0
# Matrix_before[6][5] = 2
# Matrix_before[6][7] = 2
#
# Matrix_before[7][0] = 2
# Matrix_before[7][2] = 2
# Matrix_before[7][4] = 2
# Matrix_before[7][6] = 0
#
#
# ''' Matrix_before - plansza po wykonaniu ruchu (bez zdejmowania zbitych pionków)'''
# Matrix_after = [[0 for x in range(rows)] for y in range(columns)]
#
# Matrix_after[0][1] = 1
# Matrix_after[0][3] = 1
# Matrix_after[0][5] = 1
# Matrix_after[0][7] = 1
#
# Matrix_after[1][0] = 0
# Matrix_after[1][2] = 1
# Matrix_after[1][4] = 1
# Matrix_after[1][6] = 1
#
# Matrix_after[2][1] = 1
# Matrix_after[2][3] = 0
# Matrix_after[2][5] = 1
# Matrix_after[2][7] = 3
#
# Matrix_after[3][0] = 0
# Matrix_after[3][2] = 0
# Matrix_after[3][4] = 2
# Matrix_after[3][6] = 2
#
# Matrix_after[4][1] = 2
# Matrix_after[4][3] = 0
# Matrix_after[4][5] = 0
# Matrix_after[4][7] = 0
#
# Matrix_after[5][0] = 1
# Matrix_after[5][2] = 0
# Matrix_after[5][4] = 2
# Matrix_after[5][6] = 2
#
# Matrix_after[6][1] = 0
# Matrix_after[6][3] = 0
# Matrix_after[6][5] = 2
# Matrix_after[6][7] = 2
#
# Matrix_after[7][0] = 2
# Matrix_after[7][2] = 2
# Matrix_after[7][4] = 2
# Matrix_after[7][6] = 0
#
# player_2 = False;
# player_1 = True;

#########################################################################################################

def explore(matrix):
    '''Iteracja po tablicy'''
    for i, row in enumerate(matrix):
        for j, int in enumerate(row):
            yield i, j, int


#########################################################################################################

letters = ["H", "G", "F", "E", "D", "C", "B", "A"]  # tekstowe odpowiedniki pierwszej współrzędnej

'''Klasa współrzędne - przechowuje współrzędne i, j pola'''


class Coordinates:
    def __init__(self, row, column):
        self.i = row
        self.j = column

    '''Funkcja zwracająca tekstowe współrzedne planszy np. (0,0) to H1'''

    def to_string(self):
        return letters[self.j] + str(self.i + 1)


##DIRECTIONS##
NW = "northwest"
NE = "northeast"
SW = "southwest"
SE = "southeast"

#########################################################################################################

'''Klasa pionek - przechowuje informację o właścicielu pionka i czy pionek jest damką'''


class Pawn:
    def __init__(self, player, dam=False):
        self.player = player
        self.dam = dam


#########################################################################################################

'''Klasa pole - przechowuje informacje o współrzędnych pola oraz o pionku'''


class Field:
    def __init__(self, coordinates, pawn):
        self.coordinates = coordinates
        self.pawn = pawn

    '''Funkcja zwracająca współrzedne pola po przesunięciu się w odpowiadającym kierunku (NW,NE,SW,SE)'''

    def directions(self, direction, coordinates):
        if direction == NW:
            co = Coordinates(coordinates.i - 1, coordinates.j - 1)
            return co
        elif direction == NE:
            co = Coordinates(coordinates.i - 1, coordinates.j + 1)
            return co
        elif direction == SW:
            co = Coordinates(coordinates.i + 1, coordinates.j - 1)
            return co
        elif direction == SE:
            co = Coordinates(coordinates.i + 1, coordinates.j + 1)
            return co
        else:
            return 0


#########################################################################################################

'''Funkcja przetwarzająca macierz na listę pól '''


def field_from_matrix(M1):
    fields = []
    print('M1')
    print(M1)
    for i in range(0, len(M1)):
        for j in range(0, len(M1[i])):
            co = Coordinates(i, j)
            if M1[i][j] == 1:
                pwn = Pawn(1, False)
            elif M1[i][j] == 2:
                pwn = Pawn(2, False)
            elif M1[i][j] == 3:
                pwn = Pawn(3, True)
            elif M1[i][j] == 4:
                pwn = Pawn(4, True)
            elif M1[i][j] == 0:
                pwn = Pawn(0, False)
            fields.append(Field(co, pwn))
    return fields


#########################################################################################################

'''Funkcja przeszukująca listę pól fields w celu znalezienia pola o podanych współrzędnych coord.
 Zwraca znalezione pole.'''


def Find_field(fields, coord):
    for x in fields:
        if x.coordinates.i == coord.i and x.coordinates.j == coord.j:
            return Field(x.coordinates, x.pawn)
    else:
        print("Not exist")


#########################################################################################################

'''Funkcja przeszukująca listę pól fields w celu znalezienia pozycji pola field
 Zwraca indeks - numer pozycji na liście.'''


def Find_index(fields, field):
    ind = -1
    for x in fields:
        ind = ind + 1
        if x.coordinates.i == field.coordinates.i and x.coordinates.j == field.coordinates.j and x.pawn.player == field.pawn.player and x.pawn.dam == field.pawn.dam:
            return ind
    else:
        print("Not exist")


#########################################################################################################

'''Funkcja sprawdzająca czy współrzędne coordinates znajdują się w zakresie planszy.
 Zwraca wartość True lub False'''


def in_range(coordinates):
    if coordinates.i < 0 or coordinates.j < 0 or coordinates.i > 7 or coordinates.j > 7:
        return False
    else:
        return True


#########################################################################################################

moves = []
moves_dam = []
hoop = False  # zmienna przechowująca informacje, czy jest bicie

'''Funkcja zmieniająca zmienną bicie na True.'''


def hoops():
    global hoop
    hoop = True


out_loop = False


def out_t():
    global out_loop
    out_loop = True


def out_f():
    global out_loop
    out_loop = False


'''Lista pojedynczych ruchów damki'''
global one_step
one_step = []

#########################################################################################################

'''Funkcja wyszukująca możliwe do wykonania ruchy.
 Zwraca listę ruchów postaci: A1 G2 C5'''


def return_correct_moves(Matrix_before, player):
    if player == 1 or player == 2:
        moves.clear()
        moves_dam.clear()
        one_step.clear()
        fld = field_from_matrix(Matrix_before)
        global hoop
        hoop = False
        correct_move(Matrix_before, player, fld)  # sprawdzenie dostępnych ruchów dla zwykłych pionków
        fld = field_from_matrix(Matrix_before)
        correct_move_dam(Matrix_before, player + 2, fld)  # sprawdzenie dostępnych ruchów dla damek

        moves_copy = copy.copy(moves)
        one_step_copy = copy.copy(one_step)
        moves_dam_copy = copy.copy(moves_dam)

        if player == 1 or player == 3:
            for m in moves_copy:
                if len(m) == 5 and (int(m[1]) > int(m[4]) and int(m[1]) - int(m[4]) == 1):
                    moves.remove(m)
        elif player == 2 or player == 4:
            for m in moves_copy:
                if len(m) == 5 and (int(m[4]) > int(m[1]) and int(m[4]) - int(m[1]) == 1):
                    moves.remove(m)

        if (hoop):  # postępowanie w przypadku wystąpienia bicia
            print("Jump!!")
            moves_copy = copy.copy(moves)
            for m in moves_copy:
                if len(m) == 5 and ((int(m[1]) - int(m[4])) == 1 or (int(m[4]) - int(m[1])) == 1):
                    moves.remove(m)  # usunięcie pojedynczych ruchów zwykłego pionka

            for m in one_step_copy:
                if m in moves_dam_copy:
                    moves_dam.remove(m)  # usunięcie pojedynczych ruchów damki

            moves.extend(moves_dam)  # dołączenie możliwych ruchów damek do listy ruchów zwykłego pionka
        else:
            moves.extend(one_step)
            print("Not jump.")
    return moves


#########################################################################################################

'''Funkcja sprwadzająca dostępne ruchy zwykłego pionka dla gracza player na planszy fields.
 Zwraca listę ruchów dla zwykłego pionka'''


def correct_move(Matrix_before, player, fields, reccursion=False):
    test = False
    fld = field_from_matrix(Matrix_before)
    dam = False
    indeks = -1
    for x in fields:
        if x.pawn.player == player and not test:
            current = x.coordinates.to_string()
            if len(moves) != 0:
                for m in moves:
                    if m.find(current) == len(m) - len(current):
                        indeks = moves.index(m) if m in moves else -1
                        test = True
            else:
                indeks = -1

            ##NE direction
            ne = x.directions(NE, x.coordinates)
            if in_range(ne):
                next_field = Find_field(fields, ne)
                if next_field.pawn.player == 0 and not reccursion:
                    move = next_field.coordinates.to_string()
                    if indeks >= 0:
                        moves.append(moves[indeks] + " " + move)
                    else:
                        moves.append(current + " " + move)
                elif next_field.pawn.player > 0 and next_field.pawn.player != x.pawn.player and next_field.pawn.player != x.pawn.player + 2 and next_field.pawn.player != x.pawn.player - 2:
                    ne = next_field.directions(NE, next_field.coordinates)
                    if in_range(ne):
                        double = Find_field(fld, ne)
                        if double.pawn.player == 0:
                            move = double.coordinates.to_string()
                            if indeks >= 0:
                                moves.append(moves[indeks] + " " + move)
                            else:
                                moves.append(current + " " + move)
                            fields_rec = copy.deepcopy(fields)
                            x_index = Find_index(fields, x)
                            fields_rec[x_index] = Field(x.coordinates, Pawn(0, False))
                            next_index = Find_index(fields, next_field)
                            fields_rec[next_index] = Field(next_field.coordinates, Pawn(0, False))
                            double_index = Find_index(fields, double)
                            fields_rec[double_index] = Field(double.coordinates, Pawn(player, dam))
                            hoops()
                            correct_move(player, fields_rec, True)

            ##NW direction
            nw = x.directions(NW, x.coordinates)
            if in_range(nw):
                next_field = Find_field(fields, nw)
                if next_field.pawn.player == 0 and not reccursion:
                    move = next_field.coordinates.to_string()
                    if indeks >= 0:
                        moves.append(moves[indeks] + " " + move)
                    else:
                        moves.append(current + " " + move)
                elif next_field.pawn.player > 0 and next_field.pawn.player != x.pawn.player and next_field.pawn.player != x.pawn.player + 2 and next_field.pawn.player != x.pawn.player - 2:
                    nw = next_field.directions(NW, next_field.coordinates)
                    if in_range(nw):
                        double = Find_field(fld, nw)
                        if double.pawn.player == 0:
                            move = double.coordinates.to_string()
                            if indeks >= 0:
                                moves.append(moves[indeks] + " " + move)
                            else:
                                moves.append(current + " " + move)
                            fields_rec = copy.deepcopy(fields)
                            x_index = Find_index(fields, x)
                            fields_rec[x_index] = Field(x.coordinates, Pawn(0, False))
                            next_index = Find_index(fields, next_field)
                            fields_rec[next_index] = Field(next_field.coordinates, Pawn(0, False))
                            double_index = Find_index(fields, double)
                            fields_rec[double_index] = Field(double.coordinates, Pawn(player, dam))
                            hoops()
                            correct_move(player, fields_rec, True)

            ##SE direction
            se = x.directions(SE, x.coordinates)
            if in_range(se):
                next_field = Find_field(fields, se)
                if next_field.pawn.player == 0 and not reccursion:
                    move = next_field.coordinates.to_string()
                    if indeks >= 0:
                        moves.append(moves[indeks] + " " + move)
                    else:
                        moves.append(current + " " + move)
                elif next_field.pawn.player > 0 and next_field.pawn.player != x.pawn.player and next_field.pawn.player != x.pawn.player + 2 and next_field.pawn.player != x.pawn.player - 2:
                    se = next_field.directions(SE, next_field.coordinates)
                    if in_range(se):
                        double = Find_field(fld, se)
                        if double.pawn.player == 0:
                            move = double.coordinates.to_string()
                            if indeks >= 0:
                                moves.append(moves[indeks] + " " + move)
                            else:
                                moves.append(current + " " + move)
                            fields_rec = copy.deepcopy(fields)
                            x_index = Find_index(fields, x)
                            fields_rec[x_index] = Field(x.coordinates, Pawn(0, False))
                            next_index = Find_index(fields, next_field)
                            fields_rec[next_index] = Field(next_field.coordinates, Pawn(0, False))
                            double_index = Find_index(fields, double)
                            fields_rec[double_index] = Field(double.coordinates, Pawn(player, dam))
                            hoops()
                            correct_move(player, fields_rec, True)

            ##SW direction
            sw = x.directions(SW, x.coordinates)
            if in_range(sw):
                next_field = Find_field(fields, sw)
                if next_field.pawn.player == 0 and not reccursion:
                    move = next_field.coordinates.to_string()
                    if indeks >= 0:
                        moves.append(moves[indeks] + " " + move)
                    else:
                        moves.append(current + " " + move)
                elif next_field.pawn.player > 0 and next_field.pawn.player != x.pawn.player and next_field.pawn.player != x.pawn.player + 2 and next_field.pawn.player != x.pawn.player - 2:
                    sw = next_field.directions(SW, next_field.coordinates)
                    if in_range(sw):
                        double = Find_field(fld, sw)
                        if double.pawn.player == 0:
                            move = double.coordinates.to_string()
                            if indeks >= 0:
                                moves.append(moves[indeks] + " " + move)
                            else:
                                moves.append(current + " " + move)
                            fields_rec = copy.deepcopy(fields)
                            x_index = Find_index(fields, x)
                            fields_rec[x_index] = Field(x.coordinates, Pawn(0, False))
                            next_index = Find_index(fields, next_field)
                            fields_rec[next_index] = Field(next_field.coordinates, Pawn(0, False))
                            double_index = Find_index(fields, double)
                            fields_rec[double_index] = Field(double.coordinates, Pawn(player, dam))
                            hoops()
                            correct_move(player, fields_rec, True)


#########################################################################################################

'''Funkcja sprwadzająca dostępne ruchy damek dla gracza player na planszy fields.
 Zwraca listę ruchów dla damek pionka'''


def correct_move_dam(Matrix_before, player, fields, reccursion=False):
    test = False
    fld = field_from_matrix(Matrix_before)
    global one_step
    out_f()
    dam = True
    indeks = -1
    for x in fields:
        if x.pawn.player == player and not test:
            current = x.coordinates.to_string()
            if len(moves_dam) != 0:
                for m in moves_dam:
                    if m.find(current) == len(m) - len(current):
                        indeks = moves_dam.index(m) if m in moves_dam else -1
                        test = True
            else:
                indeks = -1

            ##NE direction
            ne = x.directions(NE, x.coordinates)
            if in_range(ne):
                next_field = Find_field(fields, ne)
                while next_field.pawn.player == 0 and not reccursion and not out_loop:
                    move = next_field.coordinates.to_string()
                    if indeks >= 0:
                        moves_dam.append(moves_dam[indeks] + " " + move)
                    else:
                        moves_dam.append(current + " " + move)
                        one_step.append(current + " " + move)
                    ne = next_field.directions(NE, next_field.coordinates)
                    if in_range(ne):
                        next_field = Find_field(fields, ne)
                    else:
                        out_t()
                ne = next_field.directions(NE, next_field.coordinates)
                while next_field.pawn.player == 0 and in_range(ne):
                    next_field = Find_field(fld, ne)
                    ne = next_field.directions(NE, next_field.coordinates)
                if next_field.pawn.player > 0 and next_field.pawn.player != x.pawn.player and next_field.pawn.player != x.pawn.player + 2 and next_field.pawn.player != x.pawn.player - 2:
                    if in_range(ne):
                        double = Find_field(fld, ne)
                        if double.pawn.player == 0:
                            move = double.coordinates.to_string()
                            if indeks >= 0:
                                moves_dam.append(moves_dam[indeks] + " " + move)
                            else:
                                moves_dam.append(current + " " + move)
                            fields_rec = copy.deepcopy(fields)
                            x_index = Find_index(fields, x)
                            fields_rec[x_index] = Field(x.coordinates, Pawn(0, False))
                            next_index = Find_index(fields, next_field)
                            if next_index == None:
                                moves_dam.pop()
                                break
                            else:
                                fields_rec[next_index] = Field(next_field.coordinates, Pawn(0, False))
                                double_index = Find_index(fields, double)
                                fields_rec[double_index] = Field(double.coordinates, Pawn(player, dam))
                                hoops()
                                correct_move_dam(player, fields_rec, True)

            ##NW direction
            out_f()
            nw = x.directions(NW, x.coordinates)
            if in_range(nw):
                next_field = Find_field(fields, nw)
                while next_field.pawn.player == 0 and not reccursion and not out_loop:
                    move = next_field.coordinates.to_string()
                    if indeks >= 0:
                        moves_dam.append(moves_dam[indeks] + " " + move)
                    else:
                        moves_dam.append(current + " " + move)
                        one_step.append(current + " " + move)
                    nw = next_field.directions(NW, next_field.coordinates)
                    if in_range(nw):
                        next_field = Find_field(fields, nw)
                    else:
                        out_t()
                nw = next_field.directions(NW, next_field.coordinates)
                while next_field.pawn.player == 0 and in_range(nw):
                    next_field = Find_field(fld, nw)
                    nw = next_field.directions(NW, next_field.coordinates)
                if next_field.pawn.player > 0 and next_field.pawn.player != x.pawn.player and next_field.pawn.player != x.pawn.player + 2 and next_field.pawn.player != x.pawn.player - 2:
                    if in_range(nw):
                        double = Find_field(fld, nw)
                        if double.pawn.player == 0:
                            move = double.coordinates.to_string()
                            if indeks >= 0:
                                moves_dam.append(moves_dam[indeks] + " " + move)
                            else:
                                moves_dam.append(current + " " + move)
                            fields_rec = copy.deepcopy(fields)
                            x_index = Find_index(fields, x)
                            fields_rec[x_index] = Field(x.coordinates, Pawn(0, False))
                            next_index = Find_index(fields, next_field)
                            if next_index == None:
                                moves_dam.pop()
                                break
                            fields_rec[next_index] = Field(next_field.coordinates, Pawn(0, False))
                            double_index = Find_index(fields, double)
                            fields_rec[double_index] = Field(double.coordinates, Pawn(player, dam))
                            hoops()
                            correct_move_dam(player, fields_rec, True)

            ##SE direction
            out_f()
            se = x.directions(SE, x.coordinates)
            if in_range(se):
                next_field = Find_field(fields, se)
                while next_field.pawn.player == 0 and not reccursion and not out_loop:
                    move = next_field.coordinates.to_string()
                    if indeks >= 0:
                        moves_dam.append(moves_dam[indeks] + " " + move)
                    else:
                        moves_dam.append(current + " " + move)
                        one_step.append(current + " " + move)
                    se = next_field.directions(SE, next_field.coordinates)
                    if in_range(se):
                        next_field = Find_field(fields, se)
                    else:
                        out_t()
                se = next_field.directions(SE, next_field.coordinates)
                while next_field.pawn.player == 0 and in_range(se):
                    next_field = Find_field(fld, se)
                    se = next_field.directions(SE, next_field.coordinates)
                if next_field.pawn.player > 0 and next_field.pawn.player != x.pawn.player and next_field.pawn.player != x.pawn.player + 2 and next_field.pawn.player != x.pawn.player - 2:
                    if in_range(se):
                        double = Find_field(fld, se)
                        if double.pawn.player == 0:
                            move = double.coordinates.to_string()
                            if indeks >= 0:
                                moves_dam.append(moves_dam[indeks] + " " + move)
                            else:
                                moves_dam.append(current + " " + move)
                            fields_rec = copy.deepcopy(fields)
                            x_index = Find_index(fields, x)
                            fields_rec[x_index] = Field(x.coordinates, Pawn(0, False))
                            next_index = Find_index(fields, next_field)
                            if next_index == None:
                                moves_dam.pop()
                                break
                            fields_rec[next_index] = Field(next_field.coordinates, Pawn(0, False))
                            double_index = Find_index(fields, double)
                            fields_rec[double_index] = Field(double.coordinates, Pawn(player, dam))
                            hoops()
                            correct_move_dam(player, fields_rec, True)

            ##SW direction
            out_f()
            sw = x.directions(SW, x.coordinates)
            if in_range(sw):
                next_field = Find_field(fields, sw)
                while next_field.pawn.player == 0 and not reccursion and not out_loop:
                    move = next_field.coordinates.to_string()
                    if indeks >= 0:
                        moves_dam.append(moves_dam[indeks] + " " + move)
                    else:
                        moves_dam.append(current + " " + move)
                        one_step.append(current + " " + move)
                    sw = next_field.directions(SW, next_field.coordinates)
                    if in_range(sw):
                        next_field = Find_field(fields, sw)
                    else:
                        out_t()
                sw = next_field.directions(SW, next_field.coordinates)
                while next_field.pawn.player == 0 and in_range(sw):
                    next_field = Find_field(fld, sw)
                    sw = next_field.directions(SW, next_field.coordinates)
                if next_field.pawn.player > 0 and next_field.pawn.player != x.pawn.player and next_field.pawn.player != x.pawn.player + 2 and next_field.pawn.player != x.pawn.player - 2:
                    if in_range(sw):
                        double = Find_field(fld, sw)
                        if double.pawn.player == 0:
                            move = double.coordinates.to_string()
                            if indeks >= 0:
                                moves_dam.append(moves_dam[indeks] + " " + move)
                            else:
                                moves_dam.append(current + " " + move)
                            fields_rec = copy.deepcopy(fields)
                            x_index = Find_index(fields, x)
                            fields_rec[x_index] = Field(x.coordinates, Pawn(0, False))
                            next_index = Find_index(fields, next_field)
                            if next_index == None:
                                moves_dam.pop()
                                break
                            fields_rec[next_index] = Field(next_field.coordinates, Pawn(0, False))
                            double_index = Find_index(fields, double)
                            fields_rec[double_index] = Field(double.coordinates, Pawn(player, dam))
                            hoops()
                            correct_move_dam(player, fields_rec, True)


#########################################################################################################

global all_moves
all_moves = []

#########################################################################################################

'''Funkcja zapisująca na liście all_moves możliwe do wykonania ruchy 
 Zwraca ostateczną listę ruchów'''


def moves_start(Matrix_before, player_1):
    print('moves_start')
    print(Matrix_before)
    if player_1:
        i = 1
    else:
        i = 2
    moves = return_correct_moves(Matrix_before, i)
    without_duplicate = []
    for d in moves:
        if d not in without_duplicate:  # usunięcie duplikatów
            without_duplicate.append(d)
    global all_moves
    all_moves = copy.copy(without_duplicate)


#########################################################################################################

'''Funkcja wyświetlająca listę możliwych ruchów oraz ich ilość
 Zwraca ostateczną listę ruchów'''


def display():
    licznik = 0
    for move in all_moves:
        licznik = licznik + 1
        print(move)
    print("Liczba możliwości: ", licznik)


#########################################################################################################

'''Główna funkcja modułu sprawdzania poprawności ruchu. 
    Porównuje planszę przed wykonaniem ruchu przez aktywnego gracza
    z planszą po wykonaniu ruchu (bez zdejmowanie zbitych pionków przeciwnika
    Sprawdza czy wykonany ruch znajduje się na liście all_moves'''


def check_move(M1, Matrix_after, p1, p2):
    moves_start(M1, p1)  # uzupełnienie listy all_moves
    display()  # wyświetlenie listy możliwych ruchów
    correct = False
    i_after = 9
    j_after = 9
    if M1 == Matrix_after:
        return print("Move not found")  # nie wykryto zmiany w planszy po wykonaniu ruchu
    else:
        for i, j, int in explore(M1):
            if M1[i][j] != Matrix_after[i][j]:
                # i_before=0
                # j_before=0
                if int != 0:
                    i_before = i
                    j_before = j
                    if p1 and (M1[i_before][j_before] == 2 or M1[i_before][j_before] == 4):
                        return (False, 'Wykonano ruch pionkiem przeciwnika. Aktywny gracz to player_1')
                    if p2 and (M1[i_before][j_before] == 1 or M1[i_before][j_before] == 3):
                        return (False, 'Wykonano ruch pionkiem przeciwnika. Aktywny gracz to player_2')
                else:
                    i_after = i
                    j_after = j
        field_from = Coordinates(i_before, j_before).to_string()  # poprzednia pozycja pionka wykonującego ruch
        field_to = Coordinates(i_after, j_after).to_string()  # aktualna pozycja pionka po wykonaniu ruchu
        print("FROM: ", field_from)
        print("TO: ", field_to)
        if field_from != None and field_to != None:
            for move in all_moves:
                if move[0] == field_from[0] and move[1] == field_from[1] and move[len(move) - 2] == field_to[0] and \
                                move[len(move) - 1] == field_to[1]:
                    correct = True
        else:
            print('Odstaw pionek')
        if correct:
            print('RUCH POPRAWNY')
            return (True, 'RUCH POPRAWNY')
        else:
            print('RUCH NIEDOZWOLONY')
            return (False, 'RUCH NIEDOZWOLONY')



            # robocze ustawienie aktywnego gracza
            # player_2 = False;
            # player_1 = True;

            # check_move(Matrix_before, Matrix_after, player_1, player_2)
