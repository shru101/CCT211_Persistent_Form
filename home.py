import settings
import library
import store
from tkinter import *


class HomeScreen:
    def __init__(self):
        self.root = Tk()
        self.root.title("Home")  # Should this be changed to Fog as well?
        self.is_logged_in = True
        file = open("LIN.txt", "r")
        self.logged_in_account = file.readlines()[1][18:]

        # Frames
        self.current_frame = "home"
        self.home_frame = Frame(self.root)
        self.library_frame = Frame(self.root)
        self.store_frame = Frame(self.root)
        self.settings_frame = Frame(self.root)

        # Account Menu
        self.top = Menu(self.home_frame)
        self.root.config(menu=self.top)

        self.account_menu = Menu(self.top, tearoff=False)

        self.top.add_cascade(label="Account", menu=self.account_menu)
        self.account_menu.add_command(label="Settings", command=lambda: self.screen_switch("settings"))
        self.account_menu.add_command(label="Sign Out", command=self.sign_out)
        self.account_menu.add_command(label="Exit", command=self.root.destroy)

        # Labels
        self.welcome = Label(self.home_frame, text="Welcome back, " + self.logged_in_account)

        # Home Buttons
        button_font = ('Arial', 15)
        self.library = Button(self.home_frame, text="LIBRARY", borderwidth=5,
                              command=lambda: self.screen_switch("library"), height=2, width=25, font=button_font)

        self.store = Button(self.home_frame, text="STORE", borderwidth=5,
                            command=lambda: self.screen_switch("store"), height=2, width=25, font=button_font)

        self.p = settings.Settings(self.settings_frame, self.home_frame, self, self.logged_in_account)
        self.s = store.Store(self.store_frame, self.home_frame, self.logged_in_account, self)
        self.l = library.Library(self.library_frame, self.home_frame, self.logged_in_account, self)

        # Packing
        self.welcome.pack()

        self.library.pack()
        self.store.pack()

        self.home_frame.pack()

        self.root.mainloop()

    def screen_switch(self, next_frame):
        if self.current_frame == "home":
            self.home_frame.pack_forget()
        elif self.current_frame == "library":
            self.library_frame.pack_forget()
        elif self.current_frame == "store":
            self.store_frame.pack_forget()
        elif self.current_frame == "settings":
            self.settings_frame.pack_forget()
        if next_frame == "home":
            self.account_menu.entryconfig(0, state=NORMAL)
            self.home_frame.pack()
            self.current_frame = "home"
        elif next_frame == "library":
            self.account_menu.entryconfig(0, state=DISABLED)
            self.l.library.delete(0, END)
            self.l.display_games()
            self.library_frame.pack()
            self.current_frame = "library"
        elif next_frame == "store":
            self.account_menu.entryconfig(0, state=DISABLED)
            for row in self.s.store.get_children():
                self.s.store.delete(row)
            self.s.results()
            self.store_frame.pack()
            self.current_frame = "store"
        elif next_frame == "settings":
            self.account_menu.entryconfig(0, state=DISABLED)
            self.settings_frame.pack()
            self.current_frame = "settings"

    def sign_out(self):
        file = open('LIN.txt', 'w+')
        file.write('logged_in=NO')
        file.close()
        self.is_logged_in = False
        self.root.destroy()
