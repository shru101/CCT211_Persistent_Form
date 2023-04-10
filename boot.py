import sqlite3
import datetime
from home import HomeScreen
from tkinter import *
from PIL import ImageTk, Image

# Connect to Fog database
con = sqlite3.connect('fog.db')
c = con.cursor()


class Start:
    def __init__(self):
        self.root = Tk()
        self.root.title('Fog')
        self.isloggedin = False

        # Boot Layout
        self.foglogo_image = ImageTk.PhotoImage(Image.open("images/1x/FOG logo.png"))
        self.foglogo = Label(self.root, image=self.foglogo_image)

        self.login_signup_frame = Frame(self.root)
        self.loginbutton = Button(self.login_signup_frame, height=2, width=10, text="Log In", command=self.login)
        self.signupbutton = Button(self.login_signup_frame, height=2, width=10, text="Sign Up", command=self.sign_up)

        # Login Layout
        self.loginframe = Frame(self.root)
        self.usertext = Label(self.loginframe, text="Username")
        self.passtext = Label(self.loginframe, text="Password")
        self.username = Entry(self.loginframe)
        self.password = Entry(self.loginframe, show="*")
        self.back = Button(self.loginframe, text="Back", command=self.back)
        self.next = Button(self.loginframe, text="Next", command=self.loggedin)

        # Packing Boot layout
        self.foglogo.pack()
        self.loginbutton.pack(side=LEFT)
        self.signupbutton.pack(side=LEFT)
        self.login_signup_frame.pack()

        # Packing on to Login Frame
        self.usertext.pack()
        self.username.pack()
        self.passtext.pack()
        self.password.pack()
        self.back.pack()
        self.next.pack()

        # Run GUI
        self.logged_in_on_startup()
        self.root.mainloop()

    def logged_in_on_startup(self):
        file = open('LIN.txt', 'r')
        logged_in = file.readline().strip()
        if logged_in[-3:] == "YES":
            file.close()
            self.isloggedin = True
            self.close()

    @staticmethod
    def sign_up():
        SignUp()

    def loggedin(self):
        # FOUND FROM ONLINE AND ADAPTED
        c.execute('''SELECT * FROM Accounts WHERE Username=?''', (self.username.get(),))  # Why the comma afterwards?
        userveri = c.fetchone()
        c.execute('''SELECT * FROM Accounts WHERE Password = ?''', (self.password.get(),))
        passveri = c.fetchone()

        if userveri is not None and passveri is not None:
            file = open('LIN.txt', 'w+')
            file.write('logged_in=YES\n')
            file.write('logged_in_account=' + userveri[1])
            file.close()
            self.isloggedin = True
            self.close()

    def close(self):
        # Knowledge gained from CHATGPT
        self.root.destroy()

    def login(self):
        self.login_signup_frame.pack_forget()
        self.loginframe.pack()

    def back(self):
        self.loginframe.pack_forget()
        self.login_signup_frame.pack()


class SignUp:
    def __init__(self):
        self.root = Tk()

        # Text Input Fields
        self.usertext = Label(self.root, text="Username")
        self.username = Entry(self.root)
        self.usererror = Label(self.root, text="")

        self.passtext = Label(self.root, text="Password")
        self.password = Entry(self.root)
        self.passerror = Label(self.root, text="")

        self.passcontext = Label(self.root, text="Confirm Password")
        self.passconfirm = Entry(self.root)
        self.passconerror = Label(self.root, text="")

        self.birthday = Label(self.root, text="Birthday (YYYY-MM-DD)")
        self.bdayinput = Entry(self.root, validate="key")
        self.bdayerror = Label(self.root, text="")
        # THIS WAS CREATED USING THE HELP OF CHATGPT
        self.bdayinput.config(validatecommand=(self.bdayinput.register(lambda text: len(text) <= 10), '%P'))

        # Buttons
        self.back = Button(self.root, text="Back", command=self.close)
        self.confirm = Button(self.root, text="Confirm", command=self.confirm)

        # Packing
        self.usertext.pack()
        self.username.pack()
        self.usererror.pack()

        self.passtext.pack()
        self.password.pack()
        self.passerror.pack()

        self.passcontext.pack()
        self.passconfirm.pack()
        self.passconerror.pack()

        self.birthday.pack()
        self.bdayinput.pack()
        self.bdayerror.pack()

        self.back.pack()
        self.confirm.pack()

        # Binding
        self.bdayinput.bind("<KeyRelease>", self.bday_spacing)

        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def confirm(self):
        c.execute('''SELECT * FROM Accounts WHERE Username=?''', (self.username.get(),))  # Why the comma afterwards?
        userveri = c.fetchone()
        bday = self.bdayinput.get()
        if bday is None:
            bday = '0000-00-00'
        bday = (int(bday[:4]), int(bday[5:7]), int(bday[-2:]))
        year_restrict = datetime.datetime.now().year - 13
        if self.username.get() == "":
            self.usererror.config(text="Invalid Username", fg="red")
            self.usererror.pack()
        elif userveri is not None:
            self.usererror.config(text="Username Already Exists", fg="red")
            self.usererror.pack()
        elif self.password.get() == "":
            self.passerror.config(text="Invalid Password", fg="red")
            self.passerror.pack()
        elif self.password.get() != self.passconfirm.get():
            self.passerror.config(text="Password Doesn't Match", fg="red")
            self.passconerror.config(text="Password Doesn't Match", fg="red")
            self.passerror.pack()
            self.passconerror.pack()
        elif not ((1922 < bday[0] <= year_restrict)\
                and (0 < bday[1] < 13)\
                and (0 < bday[2] < 32)):
            self.bdayerror.config(text="Invalid Date", fg="red")
            self.bdayerror.pack()
            self.bdayinput.delete(0, END)
        else:
            c.execute('''INSERT INTO Accounts(Username, Password, Birthday)
             VALUES (?,?,?)''', (self.username.get(), self.password.get(), self.bdayinput.get()))
            con.commit()
            self.root.destroy()

    def bday_spacing(self, event):
        if len(self.bdayinput.get()) == 4:
            self.bdayinput.insert(END, "-")
        if len(self.bdayinput.get()) == 7:
            self.bdayinput.insert(END, "-")