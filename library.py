import sqlite3
from tkinter import *
from tkinter import messagebox

con = sqlite3.connect("fog.db")
c = con.cursor()


class Library:
    def __init__(self, root: Frame, home_frame: Frame, logged_in_account, home):
        self.root = root
        self.home_frame = home_frame
        self.logged_in_account = logged_in_account
        self.home = home

        # Listbox Library
        self.library = Listbox(self.root)
        self.library_scroll = Scrollbar(self.root)

        # Buttons
        self.play_button = Button(self.root, text="Play", command=self.prototype)
        self.remove_button = Button(self.root, text="Remove", command=self.remove)
        self.back_button = Button(self.root, text="Back", command=self.back)

        self.library.config(yscrollcommand=self.library_scroll.set)
        self.library_scroll.config(command=self.library.yview)

        # Packing
        self.library.pack(side=LEFT)
        self.library_scroll.pack(side=LEFT, fill=Y)
        self.play_button.pack()
        self.remove_button.pack()
        self.back_button.pack()
        self.display_games()

    def back(self):
        self.home.screen_switch('home')

    def fetch_games(self):
        c.execute('''SELECT Games FROM Accounts WHERE Username=?''', (self.logged_in_account,))
        games = c.fetchall()
        if games[0][0] is None:
            return
        games = games[0][0].split(',')
        games = games[:-1]
        return games

    def display_games(self):
        games = self.fetch_games()
        if not games:
            return
        for game in games:
            c.execute('''SELECT * FROM Games WHERE Game_Id =?''', (game,))
            game_name = c.fetchone()
            game_name = game_name[1]
            self.library.insert(END, game_name)

    def remove(self):
        tmp = self.library.curselection()
        if tmp == ():
            return
        game_name = self.library.get(tmp)
        c.execute('''SELECT Game_Id FROM Games WHERE Name=?''', (game_name,))
        game_id = str(c.fetchone()[0]) + ","
        games = ",".join(self.fetch_games()) + ','
        games = games.replace(game_id, "")
        c.execute('''UPDATE Accounts SET Games=? WHERE Username=?''', (games, self.logged_in_account))
        con.commit()
        self.library.delete(0, END)
        self.display_games()

    @staticmethod
    def prototype():
        messagebox.showinfo("Information", "This function is unavailable in this build.")
