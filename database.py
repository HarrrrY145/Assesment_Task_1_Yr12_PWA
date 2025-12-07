import sqlite3 

X = True

connection = sqlite3.Connection('LoginData.db')
cursor = connection.cursor()

cmd1 = """ CREATE TABLE IF NOT EXISTS USERS (UNIQUE_ID INT primary key,
                                        login_ID varchar(50),
                                        password varchar(50) not null)"""
cursor.execute(cmd1)


check_Users = """SELECT * FROM USERS""" 
cursor.execute(check_Users)
i = cursor.fetchone() 


cmd2 = """INSERT INTO USERS (login_ID,password)values('tester','testerP')"""
cursor.execute(cmd2)
    

inventory_database = """ CREATE TABLE IF NOT EXISTS INVENTORY ( UNIQUE_SERIAL_NUMBER INT primary key,
                                                                Store varchar(50),
                                                                Product_Name varchar(100),
                                                                Quantity INT,
                                                                Price DECIMAL(10,2), 
                                                                Average_Stock INT)"""
cursor.execute(inventory_database)




check_Inventory = """SELECT * FROM INVENTORY""" 
cursor.execute(check_Inventory)
x = cursor.fetchone() 
cursor.execute("""INSERT INTO INVENTORY (Store,Product_Name,Quantity,Price,Average_Stock)
                    values('testLocation','testName',0,0.00,0)""")

connection.commit()



user_list = cursor.execute("select * from USERS").fetchall()
inventory_list = cursor.execute("select * from INVENTORY").fetchall()

print('USER DATA BASE')
for i in user_list:
    print(i)
    
print('INVENTORY DATA BASE')
for i in inventory_list:
    print(i)
