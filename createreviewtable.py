import sqlite3
conn=sqlite3.connect('minidatabase.db')
print ("opened database successfully")
conn.execute(
	'CREATE TABLE reviews(email VARCHAR NOT NULL,net VARCHAR NOT NULL, review VARCHAR NOT NULL, res VARCHAR NOT NULL)')
print("table created successfully")
conn.close()