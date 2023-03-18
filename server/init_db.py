import sqlite3

conn = sqlite3.connect("users.db")
conn.execute('''CREATE TABLE USERS (
    Username char(50),
    Password char(60));''')