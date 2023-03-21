# Login API for Feizi Lab Interview 2023

This is a Flask API and React frontend that does the following:

Create a software API that gets log in information from users:
- if the information is correct, it directs them to the next page
- if the information is incorrect, it shows an error

If the user doesn’t have an account, it directs them to a page to create an account
- Get basic user information in that page, and create an account 

Also allows login with Google.

## Instructions
### Server
- Clone this repo
- Set up a virtual environment and install the server packages
```
cd server
py -3 -m venv venv
venv/Scripts/activate

pip install Flask
pip install flask-bcrypt
pip install sqlite3

python init_db.py
```
- To start the server, run `python server.py`

### Client

- In a separate terminal and in the base directory:
- Set up front-end
```
cd client
npm i
```
- To start the client, run `npm run start`
- Go to `localhost:3000`