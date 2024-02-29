import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user="root", password ="password@123")

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE user_test")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
