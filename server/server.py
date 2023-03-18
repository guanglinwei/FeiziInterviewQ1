from flask import Flask, request, g
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = "test secret key"

def get_db() -> sqlite3.Connection:
    # Connect to the database
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("users.db")
        
    return db

# When the user submits the login form, this is where the data is sent
@app.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    
    db = get_db()
    
    user = db.execute("SELECT * FROM USERS WHERE username = ?;", (username,)).fetchone()
    if user is None:
        # Account does not exist, so redirect to registration page
        return {
            "url": "/register",
            "state": {
                "username": username,
                "message": "User does not exist. Please create an account."
            }
        }
    else:
        # Account does exist
        password = request.json["password"]
        
        # Correct password, go to next page
        if bcrypt.check_password_hash(user[1], password):
            return {
                "url": "/user",
                "state": {
                    "username": username
                }
            }
        # Incorrect password, show error
        else:
            return {
                "url": "/",
                "state": {
                    "error": "Incorrect password."
                }
            }
    
@app.route("/register_user", methods=["POST"])
def register_user():
    username = request.json["username"]
    password = request.json["password"]
    
    db = get_db()
    
    user = db.execute("SELECT * FROM USERS WHERE username = ?;", (username,)).fetchone()
    if user is not None:
        # Account already exists
        return {
            "url": "/",
            "state": {
                "username": username,
                "message": "Account with that name already exists. Please log in."
            }
        }
    else:
        # Add new account
        print("Creating new account with name:", username)
        db.execute("INSERT INTO USERS (Username, Password) VALUES (?, ?)",
                   (username, bcrypt.generate_password_hash(password)))
        
        db.commit()
        user = db.execute("SELECT * FROM USERS WHERE username = ?;", (username,)).fetchone()
        
        return {
            "url": "/",
            "state": {
                "username": username,
                "message": "Account created. You can now log in."
            }
        }
    
    
    
@app.teardown_appcontext
def close_conn(e):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
        
if __name__ == "__main__":
    app.run()