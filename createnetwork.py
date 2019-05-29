import sqlite3
conn=sqlite3.connect('minidatabase.db')
print ("opened database successfully")
conn.execute(
	'CREATE TABLE network(name VARCHAR NOT NULL PRIMARY KEY ,country VARCHAR NOT NULL, email VARCHAR NOT NULL, password VARCHAR NOT NULL)')
print("table created successfully")
conn.close()