from flask import Flask,render_template,request
import sqlite3 as sql
from PIL import Image
import os

app=Flask(__name__)

@app.route('/')
def home():
	return render_template('homepage.html')

	
			
@app.route('/enter')
def enter():
	return render_template('homepage.html')
@app.route('/stocks')
def stocks():
	return render_template('stockinput.html')
	
	
# @app.route('/net')
# def net():
	# return render_template('review.html')

@app.route('/userlogin2')
def userlogin2():
	return render_template('login.html')
	
@app.route('/rate')
def rate():
	return render_template('rate.html')
	
	
@app.route('/best',methods=['POST','GET'])
def best():
	msg="you reviewed it as a good network"
	return render_template('result.html',msg=msg)
@app.route('/bad',methods=['POST','GET'])
def bad():
	msg="you reviewed it as a bad network"
	return render_template('result.html',msg=msg)

@app.route('/average',methods=['POST','GET'])
def average():
	msg="you reviewed it as an average network"
	return render_template('result.html',msg=msg)
	
@app.route('/worst',methods=['POST','GET'])
def worst():
	msg="you reviewed it as a worst network"
	return render_template('result.html',msg=msg)
	
@app.route('/excellent',methods=['POST','GET'])
def excellent():
	msg="you reviewed it as an excellent network"
	return render_template('result.html',msg=msg)
@app.route('/stockprediction',methods=['POST','GET'])
def stockprediction():
	if request=='POST':
		days=request.form['days']
	else:
		days=request.form['days']
	import pandas as pd
	import datetime as dt
	import numpy as np
	data_source=r'd:\dji.xlsx'
	df=pd.read_excel(data_source, index_col='Date')
	#print(df.tail())
	ndayforward=int(days)
	df['day_cng']=(df['close'].pct_change())*100
	#print(df.tail())
	df['nday_cng']=df['day_cng'].shift(-ndayforward)
	dcriteria=(df.index>='1985-01-29') & (df.index<=dt.datetime.today())
	tcriteria=df['day_cng']<-1
	criteria=(dcriteria) & (tcriteria)
	#print(df[criteria].tail())
	#msg= (df[criteria].loc[:,['close','nday_cng']].agg(['mean', 'median','std']))
	msg= (df[criteria].loc[:,['nday_cng']].agg(['mean', 'median','std']))
	return render_template('stockresult.html',msg = msg)
		
@app.route('/sentiment',methods=['POST','GET'])
def sentiment():
	if request=='POST':
		email=request.form["email"]
		net=request.form["net"]
		review=request.form['review']
	else:
		email=request.form["email"]
		net=request.form["net"]
		review=request.form['review']
	#msg2=print (review)
	import numpy as np
	import pandas as pd
	import nltk
	from nltk.corpus import stopwords
	from sklearn.feature_extraction.text import TfidfVectorizer
	from sklearn.cross_validation import train_test_split
	from sklearn import naive_bayes
	from sklearn.metrics import roc_auc_score
	df=pd.read_csv("D:\\training.txt", sep='\t', names=['liked','txt'])
	df.head()
	stopset = set(stopwords.words('english'))
	vectorizer = TfidfVectorizer(use_idf = True, lowercase=True, strip_accents='ascii', stop_words=stopset)
	y = df.liked
	X= vectorizer.fit_transform(df.txt)
	print (y.shape)
	print (X.shape)
	X_train,X_test, y_train, y_test = train_test_split(X, y, random_state=42)
	clf = naive_bayes.MultinomialNB()
	clf.fit(X_train, y_train)
	roc_auc_score(y_test, clf.predict_proba(X_test)[:,1])
	#r="i hate it"
	#r=review
	movie_reviews_array=np.array([review])
	#movie_reviews_array=np.array(["the best movie"])
	
	
	moview_review_vector = vectorizer.transform(movie_reviews_array)
	
	print(clf.predict(moview_review_vector))
	m=(clf.predict(moview_review_vector))
	if m==0:
		res="NEGATIVE"
		
	if m==1:
		res="POSITIVE"
	addreview(email,net,review,res)
	msg="THANK YOU FOR THE REVIEW"
	return render_template('result.html',msg = msg)
	
	
	
	
#database stuff
#register new user
@app.route('/register')    # open new registration page
def new_student():
	return render_template('signup.html')
	
	
#adding user record to thr database
@app.route('/adduser',methods=['POST','GET'])	# on submit store it to the databse
def adduser():
	
	if request.method=='POST':
		#try:
			name=request.form['name']
			email=request.form['email']
			dob=request.form['dob']
			ph=request.form['ph']
			net=request.form['net']
			psw=request.form['psw']
			
			
			with sql.connect('minidatabase.db')as con:
				cur=con.cursor()
				cur.execute('INSERT INTO user(name,email,dob,ph,net,psw) VALUES(?,?,?,?,?,?)',(name,email,dob,ph,net,psw))

				
				con.commit()
				msg="User account created sucessfully"
		
			return render_template('result.html',msg = msg)
			con.close()
#user login
@app.route('/loggeduser/<name>') #homepage 
def loggeduser(name):
	return render_template('afterlogin.html',name=name)
	
@app.route('/userlogin/<name>') #homepage 
def userlogin(username):
	return render_template('afterlogin.html',name=name) 

@app.route('/signin',methods=['POST','GET']) 
def signin():
	if request.method=='POST':
		email=request.form['email']
		psw=request.form['psw']
		con=sql.connect('minidatabase.db')
		con.row_factory = sql.Row
	
		cur=con.cursor()
		cur.execute('select name,email,psw,net from user')
	
		rows=cur.fetchall();

		for row in rows:
			if(row["email"]==email and row["psw"] ==psw):
				name=row["name"]
				nets=row["net"]
				
				return render_template('afterlogin.html',name=email,net=nets,msg3=name)
		return render_template('login.html')
#counting number of users
@app.route('/numberofusers') 
def noofusers():
		con=sql.connect('minidatabase.db')
		con.row_factory = sql.Row
	
		cur=con.cursor()
		cur.execute('select * from user where net="jio"')
	
		rows=cur.fetchall();
		x=0
		for row in rows:
			x+=1
		return render_template('result.html', msg=x)
		
		
#vieww user details
@app.route('/userdetails') #homepage 
def userdetails():
	con=sql.connect('minidatabase.db')
	con.row_factory = sql.Row
	
	cur=con.cursor()
	cur.execute('select * from user')
	
	rows=cur.fetchall();
	return render_template('usertable.html',rows=rows)

#review network		
@app.route('/reviewnet/<msg2>/<msg3>')  
def reviewnet(msg2,msg3):
	return render_template('review.html',msg2=msg2,msg3=msg3)

#adding review to the table

#@app.route('/adduser',methods=['POST','GET'])	# on submit store it to the databse
def addreview(email,net,review,res):
	if request.method=='POST':
		#try:
			# name=request.form['name']
			# email=request.form['email']
			# dob=request.form['dob']
			# ph=request.form['ph']
			# net=request.form['net']
			# psw=request.form['psw']
			
			
			with sql.connect('minidatabase.db')as con:
				cur=con.cursor()
				cur.execute('INSERT INTO reviews(email,net,review, res) VALUES(?,?,?,?)',(email,net,review,res))

				
				con.commit()
				msg="User account created sucessfully"
		
			return render_template('result.html',msg = msg)
			con.close()
	
#view reviews
@app.route('/viewreviews') #homepage 
def viewreviews():
	con=sql.connect('minidatabase.db')
	con.row_factory = sql.Row
	
	cur=con.cursor()
	cur.execute('select *from reviews')
	
	rows=cur.fetchall();
	return render_template('reviewtablecss.html',rows=rows)
	
	
#NETWORKS
@app.route('/registernet')	
def registernet():
	return render_template('registernet.html')

@app.route('/addnetwork',methods=['POST','GET'])	# on submit store it to the databse
def addnetwork():
	
	if request.method=='POST':
		#try:
			name=request.form['name']
			country=request.form['country']
			email=request.form['email']
			password=request.form['password']
			
			
			with sql.connect('minidatabase.db')as con:
				cur=con.cursor()
				cur.execute('INSERT INTO network(name,country,email,password) VALUES(?,?,?,?)',(name,country,email,password))

				
				con.commit()
				msg="Network account created sucessfully"
		
			return render_template('result.html',msg = msg)
			con.close()

@app.route('/loggednetwork/<name>') #homepage 
def loggednet(name):
	return render_template('afternetlogin.html',name=name)
	
@app.route('/netlogin/<name>') #homepage 
def nettlogin(username):
	return render_template('afternetlogin.html',name=name) 
	
#network login
@app.route('/netlogin') 
def netlogin():
	return render_template('netlogin.html')
	
@app.route('/networklogin',methods=['POST','GET']) 
def networklogin():
	if request.method=='POST':
		name=request.form['name']
		password=request.form['password']
		con=sql.connect('minidatabase.db')
		con.row_factory = sql.Row
	
		cur=con.cursor()
		cur.execute('select name,password from network')
	
		rows=cur.fetchall();

		for row in rows:
			if(row["name"]==name and row["password"] ==password):
				
				
				return render_template('afternetlogin.html',name=name)
		return render_template('netlogin.html')
        

@app.route('/networklogin2',methods=['POST','GET']) 
def networklogin2():
	if request.method=='POST':
		name=request.form['name']
		password=request.form['password']
		con=sql.connect('minidatabase.db')
		con.row_factory = sql.Row
	
		cur=con.cursor()
		cur.execute('select name,password from network')
	
		rows=cur.fetchall();

		for row in rows:
			if(row["name"]==name and row["password"] ==password):
				list=[]
				list.append(countusers('AIRTEL'))
				list.append(countusers('VODAFONE'))
				list.append(countusers('JIO'))
				list.append(countusers('IDEA'))
				sum=totalusers()
				msg1=(list[0]/sum)*360
				msg2=(list[1]/sum)*360
				msg3=(list[2]/sum)*360
				msg4=(list[3]/sum)*360
				
                
				
				
				return render_template('afternetlogin.html',name=name,msg1=msg1,msg2=msg2,msg3=msg3,msg4=msg4)
		return render_template('netlogin.html')
@app.route('/userscount/<name>') 
def userscount(name):
		con=sql.connect('minidatabase.db')
		con.row_factory = sql.Row
	
		cur=con.cursor()
		cur.execute('select * from user where net=?',(name,))
	
		rows=cur.fetchall();
		x=0
		for row in rows:
			x+=1
		return render_template('result.html', msg=x)
@app.route('/addplans/<msg1>')  
def addplans(msg1):
	return render_template('addplans.html',msg1=msg1)


@app.route('/storeplans',methods=['POST','GET']) 
def storeplans():
		if request.method=='POST':
		#try:
			name=request.form['name']
			price=request.form['price']
			data=request.form['data']
		
		
			with sql.connect('minidatabase.db')as con:
				cur=con.cursor()
				cur.execute('INSERT INTO plan(name,price,data) VALUES(?,?,?)',(name,price,data))

				
				con.commit()
				msg="plan added successfully"
		
			return render_template('result.html',msg = msg)
			con.close()
			
#view plans
@app.route('/plans/<net>') #homepage 
def plans(net):
	con=sql.connect('minidatabase.db')
	con.row_factory = sql.Row
	
	cur=con.cursor()
	cur.execute('select * from plan where name=?',(net,))
	# cur.execute('select * from plan')
	rows=cur.fetchall();
	return render_template('plantable.html',rows=rows)
	
@app.route('/allplans') #homepage 
def allplans(net):
	con=sql.connect('minidatabase.db')
	con.row_factory = sql.Row
	
	cur=con.cursor()
	#cur.execute('select * from plan where name=?',(net,))
	cur.execute('select * from plan')
	rows=cur.fetchall();
	return render_template('plantable.html',rows=rows)
	
def totalusers():
    con=sql.connect('minidatabase.db')
    con.row_factory = sql.Row
	
    cur=con.cursor()
    cur.execute('select * from user')
	
    rows=cur.fetchall();
    x=0
    for row in rows:
        x+=1
    return x
def countusers(name):
    con=sql.connect('minidatabase.db')
    con.row_factory = sql.Row
	
    cur=con.cursor()
    cur.execute('select * from user where net=?',(name,))
	
    rows=cur.fetchall();
    x=0
    for row in rows:
        x+=1
    return x

    
	
#CHARTS
@app.route("/charts")
def charts():
    list=[]
    list.append(countusers('AIRTEL'))
    list.append(countusers('VODAFONE'))
    list.append(countusers('JIO'))
    list.append(countusers('IDEA'))
    sum=totalusers()
    msg1=(list[0]/sum)*360
    msg2=(list[1]/sum)*360
    msg3=(list[2]/sum)*360
    msg4=(list[3]/sum)*360
    return render_template('chart.html', msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4)
			
if __name__=='__main__':
	app.run(debug=True)

	
	
	
	
	
	
	
	