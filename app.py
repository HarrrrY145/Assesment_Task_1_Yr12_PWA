print("http://localhost:8080/")
print("http://localhost:8080/userHome")


from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os
from waitress import serve 




app = Flask(__name__)
app.secret_key = os.urandom(24)

# Routing the user to the login page. 


#Getting all from the inventory table
def get_inventory_table():
    conn = sqlite3.connect("LoginData.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM INVENTORY;")
    row = cursor.fetchall()
    conn.close()
    return row

# Getting all from the users 
def get_user_table():
    conn = sqlite3.connect("LoginData.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS;")
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

    user = cursor.execute("SELECT UNIQUE_ID, Admin, login_ID FROM USERS WHERE login_ID=? AND password=?", (login_ID,password)).fetchone()
    
    #if user exists
    if user: 
        session['user_id'] = user [0]
        session['is_admin'] = bool(user[1])
        session['login_ID'] = user [2]

        return redirect("/userHome")
    
    else:
        return redirect('/')
    



@app.route("/adminPage", methods=["GET","POST"])
def admin_page():
    if not session.get('is_admin'):
        return "Access Denied: Admins Only", 403
    
    item = get_user_table()
    return render_template("adminPage.html", item=item)



@app.route('/verification')
def signUp():
    return render_template('verification.html')

@app.route('/newUser')
def newUser():
    return render_template('newUser.html')

@app.route('/adminCreateUser')
def adminCreateUser():
    return render_template('adminCreateUser.html')

@app.route('/addInventory')
def addInventory():
    return render_template('addInventory.html')




@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    serialNumber = request.form.get('Serial_Number')
    productName =request.form.get('Product_Name')
    quantity = request.form.get('Quantity')
    price =request.form.get('Price')
    store =request.form.get('Store')
    
    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    ans = cursor.execute("select * from INVENTORY where Serial_Number=? AND Store=? AND Product_Name=? AND Quantity=? AND Price=?",(serialNumber,store,productName,quantity,price)).fetchall()

    if len(ans) > 0:
        connection.close()
        return render_template('addInventory.html')
    else:
        cursor.execute("INSERT INTO INVENTORY(Serial_Number,Store,Product_Name,Quantity,Price)values(?,?,?,?,?)",(serialNumber,store,productName,quantity,price))
        connection.commit()
        connection.close()
        return redirect('/userHome')
        


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
    

@app.route('/admin_add_user', methods=['POST'])
def admin_add_user():
    Login_ID = request.form.get('Login_ID')
    password =request.form.get('password')
    role = request.form.get('role')

    is_admin = True if role == "Admin" else False
    
    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    ans = cursor.execute("select * from USERS where Login_ID=? AND password=?",(Login_ID,password)).fetchall()

    if len(ans) > 0:
        connection.close()
        return render_template('adminPage.html')
    else:
        cursor.execute("INSERT INTO USERS(Admin, Login_ID, password)values(?,?,?)",(is_admin,Login_ID,password))
        connection.commit()
        connection.close()
        item = get_user_table()
        return render_template("adminPage.html", item=item)

#Deleting users and Inventory:
@app.route("/delete_user/<int:user_id>", methods=['POST'])
def delete_user(user_id):
    conn = sqlite3.connect("LoginData.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM USERS WHERE UNIQUE_ID = ?", (user_id,))

    conn.commit()
    conn.close()
    return redirect(url_for("admin_page"))


@app.route("/delete_inventory", methods=['POST'])
def delete_inventory():
    id_list = request.form.getlist("delete_ids")
    print(id_list)

    if not id_list:
        return redirect(url_for("inventory_table"))
    
    conn = sqlite3.connect("LoginData.db")
    cursor = conn.cursor()

    cursor.executemany("DELETE FROM INVENTORY WHERE UNIQUE_SERIAL_NUMBER = ?", [(i,) for i in id_list])

    conn.commit()
    conn.close()
    return redirect(url_for("inventory_table"))


@app.route("/UpdateRole/<int:user_id>", methods=['POST'])
def UpdateRole(user_id):
    conn = sqlite3.connect("LoginData.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE USERS SET Admin = 1 WHERE UNIQUE_ID = ?", (user_id,)) 
    conn.commit()
    conn.close()
    return redirect(url_for("admin_page"))









if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)

