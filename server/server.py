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
    is_google_login = request.json.get("isGoogleLogin")
    
    db = get_db()
    
    # for x in db.execute("SELECT * FROM USERS").fetchall():
    #     print(x)
    
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
        
        # Account was made with Google
        if user[2] == 1:
            # Tried to log in with username and password on Google account
            if is_google_login != 1:
                return {
                    "url": "/",
                    "state": {
                        "error": "Must log in to that user with Google."
                    }
                }
            else:
                # OAuth did not validate the login request
                if request.json.get("sub") is None or user[3] != request.json.get("sub"):
                    return {
                        "url": "/",
                        "state": {
                            "error": "An error occurred when trying to log in with Google."
                        }
                    }
                else:
                    # Successful
                    return {
                        "url": "/user",
                        "state": {
                            "username": user[0]
                        }
                    }
                    
            
        if (user[2] == 1 and is_google_login == 1) or bcrypt.check_password_hash(user[1], request.json["password"]):
            return {
                "url": "/user",
                "state": {
                    "username": user[0]
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
    password = request.json.get("password")
    is_google_login = request.json.get("isGoogleLogin")
    sub = request.json.get("sub")
    
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
        
        # Not logging in with Google
        if is_google_login is None or is_google_login == 0:
            if password is None:
                return {
                    "url": "/register",
                    "state": {
                        "error": "Password cannot be empty."
                    }
                }
            else:
                db.execute("INSERT INTO USERS (Username, Password) VALUES (?, ?)",
                        (username, bcrypt.generate_password_hash(password)))
        else:
            # Creating account with Google
            if sub is None:
                return {
                    "url": "/",
                    "state": {
                        "error": "An error occurred when creating an account with Google."
                    }
                }
            else:
                db.execute("INSERT INTO USERS (Username, IsGoogleLogin, Sub) VALUES (?, ?, ?)",
                        (username, 1, sub))
        
        db.commit()
        
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