import sqlite3
conn=sqlite3.connect('minidatabase.db')
print ("opened database successfully")
conn.execute(
	'CREATE TABLE offer(name VARCHAR NOT NULL,price VARCHAR NOT NULL, value VARCHAR, validity VARCHAR)')
print("table created successfully")
conn.close()