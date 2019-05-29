'''import sqlite3
conn=sqlite3.connect('databasemini.db')
print ("opened database successfully")
conn.execute(
	'CREATE TABLE us(name TEXT NOT NULL,email VARCHAR NOT NULL PRIMARY KEY, dob DATE NOT NULL,ph VARCHAR NOT NULL, net VARCHAR NOT NULL, password TEXT NOT NULL)')
print("table created successfully")
conn.close()'''
import sqlite3
conn=sqlite3.connect('minidatabase.db')
print ("opened database successfully")
conn.execute(
	'CREATE TABLE user(name TEXT NOT NULL,email VARCHAR NOT NULL PRIMARY KEY, dob DATE NOT NULL,ph VARCHAR NOT NULL, net VARCHAR NOT NULL, psw TEXT NOT NULL)')
print("table created successfully")
conn.close()