import sqlite3

con = sqlite3.connect("fog.db")

c = con.cursor()

# AUTO INCREMENTATION WAS FOUND ONLINE, DO WE NEED TO REFERENCE?
c.execute('''CREATE TABLE IF NOT EXISTS Accounts(Account_Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
Username TEXT NOT NULL, Password TEXT NOT NULL, Birthday DATE NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS Games(Game_Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
Name TEXT NOT NULL, Genre TEXT NOT NULL, Downloads INT NOT NULL)''')

con.commit()
