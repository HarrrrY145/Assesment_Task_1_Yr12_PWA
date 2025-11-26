from flask import Flask, render_template, request, redirect
import sqlite3
import os
from waitress import serve 

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Routing the user to the login page. 
@app.route('/') 
def login():
    return render_template('login.html')

@app.route('')

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)