from flask import Flask, render_template, request, redirect
import sqlite3
import os
from waitress import serve 


print("http://localhost:8080/")


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Routing the user to the login page. 

def get_inventory_table():
    conn = sqlite3.connect("LoginData.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM INVENTORY;")
    row = cursor.fetchall()
    conn.close()
    return row

@app.route("/userHome", methods=["GET", "POST"])
def inventory_table():
    item = get_inventory_table()
    return render_template("userHome.html", item=item)

@app.route('/') 
def login():
    return render_template('login.html')

@app.route('/login_validation', methods=['POST'])
def login_valdiation():
    login_ID = request.form.get('login_ID')
    password = request.form.get('password')

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    user = cursor.execute("SELECT * FROM USERS WHERE login_ID=? AND password=?", (login_ID,password)).fetchall()
    if len(user) > 0:
        items = get_inventory_table()
        return redirect("/userHome")
    else:
        return redirect('/')

@app.route('/verification')
def signUp():
    return render_template('verification.html')

@app.route('/newUser')
def newUser():
    return render_template('newUser.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    Login_ID = request.form.get('Login_ID')
    password =request.form.get('password')
    
    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    ans = cursor.execute("select * from USERS where Login_ID=? AND password=?",(Login_ID,password)).fetchall()

    if len(ans) > 0:
        connection.close()
        return render_template('login.html')
    else:
        cursor.execute("INSERT INTO USERS(Login_ID,password)values(?,?)",(Login_ID,password))
        connection.commit()
        connection.close()
        return render_template('login.html')


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)

