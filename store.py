import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Connect to fog database and create a cursor
con = sqlite3.connect("fog.db")
c = con.cursor()


class Store:
    def __init__(self, root: Frame, home_frame: Frame, logged_in_account, home):
        self.root = root
        self.home_frame = home_frame
        self.logged_in_account = logged_in_account
        self.home = home

        # Treeview
        self.store_scroll = Scrollbar(self.root)
        self.store = ttk.Treeview(self.root)
        self.store['columns'] = ('1', '2')
        self.store.heading('#0', text="Title")
        self.store.heading('1', text="Genre")
        self.store.heading('2', text="Downloads")

        self.back_button = Button(self.root, text="Back", command=self.back)
        self.add_button = Button(self.root, text="Add To Library", command=self.add_to_library)

        self.store.config(yscrollcommand=self.store_scroll.set)
        self.store_scroll.config(command=self.store.yview)

        self.store.pack(side=LEFT)
        self.store_scroll.pack(side=LEFT, fill=Y)
        self.add_button.pack(side=BOTTOM)
        self.back_button.pack(side=BOTTOM)
        self.results()

    def back(self):
        self.home.screen_switch('home')

    def results(self):
        c.execute('''SELECT * FROM Games''')
        games = c.fetchall()
        for game in games:
            name = game[1]
            genre = game[2]
            downloads = game[3]
            self.store.insert('', 'end', text=name, values=(genre, downloads))

    def get_tree_selection(self):
        return self.store.selection()

    def add_to_library(self):
        store_game_info = self.get_tree_selection()
        store_game_info = self.store.item(store_game_info)
        game_name = store_game_info["text"]
        c.execute('''SELECT * FROM Games WHERE Name = ?''', (game_name,))
        game_info = str(c.fetchone()[0])
        current_game_library = c.execute('''SELECT Games FROM Accounts WHERE Username=?''',
                                         (self.logged_in_account,)).fetchone()[0]
        if current_game_library is None:
            c.execute('''UPDATE Accounts SET Games=? WHERE Username=?''',
                      (game_info + ',', self.logged_in_account,))
            con.commit()
        elif game_info not in current_game_library:

            c.execute('''UPDATE Accounts SET Games=? WHERE Username=?''',
                      (current_game_library + game_info + ',', self.logged_in_account,))
            con.commit()
        else:
            messagebox.showinfo("Information", "This game is already in your library.")
