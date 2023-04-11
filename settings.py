import sqlite3
from tkinter import *
from tkinter import messagebox

con = sqlite3.connect("fog.db")
c = con.cursor()


class Settings:
    def __init__(self, root: Frame, home_frame: Frame, home, account):
        self.root = root
        self.home_frame = home_frame
        self.home = home
        self.account = account
        self.account_settings = Button(self.root, text="Account Settings", command=self.account_settings)
        self.upload_game = Button(root, text="Upload Game", command=self.upload_game)
        self.back_button = Button(root, text="Back", command=self.back)

        self.account_settings.pack()
        self.upload_game.pack()
        self.back_button.pack()

    def back(self):
        self.home.screen_switch('home')

    @staticmethod
    def upload_game():
        UploadGame()

    def account_settings(self):
        AccountSettings(self.account, self.home)


class UploadGame:
    def __init__(self):
        self.root = Tk()

        self.name_label = Label(self.root, text="Name")
        self.name_entry = Entry(self.root)

        self.genre_label = Label(self.root, text="Genre")
        self.genre_entry = Entry(self.root)

        self.file = Button(self.root, text="Select File", command=self.prototype)
        self.submit = Button(self.root, text="Submit", command=self.upload_game)

        self.name_label.pack()
        self.name_entry.pack()
        self.genre_label.pack()
        self.genre_entry.pack()
        self.file.pack()
        self.submit.pack()

        self.root.mainloop()

    @staticmethod
    def prototype():
        messagebox.showinfo("Information", "This feature is not available in this build")

    def upload_game(self):
        c.execute('''INSERT INTO Games(Name, Genre, Downloads) VALUES(?,?,0)''',
                  (self.name_entry.get(), self.genre_entry.get()))
        con.commit()
        messagebox.showinfo("Information", "Game successfully uploaded")
        self.root.destroy()


class AccountSettings:
    def __init__(self, account, home):
        self.root = Tk()
        self.account = account
        self.home = home

        self.change_password = Button(self.root, text="Change Password", command=self.password_change_form)
        self.delete_account = Button(self.root, text="Delete Account", command=self.delete_account)
        self.confirm_button = Button(self.root, text="Confirm", command=self.password_change)
        self.back_button = Button(self.root, text="Back", command=self.back)

        self.old_pass = Label(self.root, text="Old Password")
        self.new_pass = Label(self.root, text="New Password")
        self.new_pass_con = Label(self.root, text="Confirm Password")

        self.old_pass_entry = Entry(self.root)
        self.new_pass_entry = Entry(self.root)
        self.new_pass_con_entry = Entry(self.root)

        self.change_password.pack()
        self.delete_account.pack()

        self.root.mainloop()

    def password_change_form(self):
        self.change_password.pack_forget()
        self.delete_account.pack_forget()

        self.old_pass.pack()
        self.old_pass_entry.pack()
        self.new_pass.pack()
        self.new_pass_entry.pack()
        self.new_pass_con.pack()
        self.new_pass_con_entry.pack()
        self.confirm_button.pack()
        self.back_button.pack()

    def password_change(self):
        c.execute('''SELECT Password FROM Accounts WHERE Username=?''', (self.account,))
        password = c.fetchone()[0]
        if password != self.old_pass_entry.get():
            self.old_pass.config(fg="red")
        if self.new_pass_entry.get() != self.new_pass_con_entry.get():
            self.new_pass.config(fg="red")
            self.new_pass_con.config(fg="red")
        if password == self.new_pass_entry.get():
            self.new_pass.config(fg="red")
            return
        if (password == self.old_pass_entry.get()) and \
                (self.new_pass_entry.get() == self.new_pass_con_entry.get()):
            c.execute('''UPDATE Accounts SET Password=? WHERE Username=?''',
                      (self.new_pass_entry.get(), self.account,))
            con.commit()
            self.root.destroy()

    def back(self):
        self.old_pass.pack_forget()
        self.old_pass_entry.pack_forget()
        self.new_pass.pack_forget()
        self.new_pass_entry.pack_forget()
        self.new_pass_con.pack_forget()
        self.new_pass_con_entry.pack_forget()
        self.confirm_button.pack_forget()
        self.back_button.pack_forget()

        self.change_password.pack()
        self.delete_account.pack()

    def delete_account(self):
        response = messagebox.askyesno("Warning", "Are you sure you want to delete your account?")
        if response:
            c.execute('''DELETE FROM Accounts WHERE Username=?''', (self.account,))
            con.commit()
            self.root.destroy()
            self.home.sign_out()
