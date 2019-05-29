# import sqlite3
# conn=sqlite3.connect('minidatabase.db')
# print ("opened database successfully")
# conn.execute(
	# 'CREATE TABLE plans(name VARCHAR NOT NULL,plan VARCHAR NOT NULL)')
# print("table created successfully")
# conn.close()
import sqlite3
conn=sqlite3.connect('minidatabase.db')
print ("opened database successfully")
conn.execute(
	'CREATE TABLE plan(name VARCHAR NOT NULL,price INTEGER NOT NULL, data VARCHAR)')
print("table created successfully")
conn.close()