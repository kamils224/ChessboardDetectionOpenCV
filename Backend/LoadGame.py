import json
import os
import tkinter
from tkinter import filedialog

class LoadGame(): #klasa wczytująca rozgrywke
    def __init__(self,path):
        path = self.askAboutDirector()
        data = open(path, 'r').read() #wczytaj z pliku
        parsed_json = json.loads(data)  #sformatuj do json
        self.game_name = parsed_json["game_name"]   # do zmiennej game_name zapisz nazwa
        self.game_history = parsed_json["game_history"]  # zapisuje historie rozgrywki
        self.game_date = parsed_json["date"]     #zapisuje date
        self.player_1_name = parsed_json["player1_name"] # zapisuje gracza 1 (pierwszy sie rusze)
        self.player_2_name = parsed_json["player2_name"] # drugi sie rusza gracz 2

    def return_round(self, round_number): # zwraca macierz obrazującą plansze w danej rundzie,
        if round_number >= len(self.game_history) or round_number < 0:
            print("W historii nie ma takiej rundy")
        else:
            return self.game_history[round_number]["pawns"]#z historii bierze odpowiednią runde i zwraca macierz planszy

    def askAboutDirector(self):
        root = tkinter.Tk()
        root.withdraw()  # use to hide tkinter window

        currdir = os.getcwd()
        outFileName = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Select file',
                                               filetypes=[('txt files', '.txt')], defaultextension='.txt')
        return outFileName