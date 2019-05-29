import sqlite3
conn=sqlite3.connect('minidatabase.db')
print ("opened database successfully")
x='AIRTEL'
conn.execute(
	'DELETE from reviews where net= ?',(x,))
print("table created successfully")
conn.close()