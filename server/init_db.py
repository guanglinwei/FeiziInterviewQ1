import sqlite3

conn = sqlite3.connect("users.db")
# conn.execute("DROP TABLE USERS")
# conn.commit()
conn.execute('''CREATE TABLE USERS (
    Username varchar(50),
    Password varchar(60),
    IsGoogleLogin Bit NOT NULL DEFAULT(0),
    Sub varchar(32));''')

# conn.execute("INSERT INTO USERS (Username, Password, IsGoogleLogin, Sub) VALUES (?, ?, ?, ?)", ("user1", "pass1", 1, 123123123))
# conn.commit()

# for x in conn.execute("SELECT * FROM USERS").fetchall():
#     print(x)