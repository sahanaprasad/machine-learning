from flask import Flask,render_template,request
import sqlite3 as sql
from PIL import Image
import os

app=Flask(__name__)

@app.route('/')
def home():
	return render_template('homepage.html')

	
			
@app.route('/enter',methods=['POST','GET'])
def enter():
	render_template('review.html')
@app.route('/sentiment',methods=['POST','GET'])
def sentiment():
	if request=='POST':
		review=request.form['review']
	msg2=print (review)
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
	r="i hate it"
	#r=review
	movie_reviews_array=np.array([r])
	#movie_reviews_array=np.array(["the best movie"])
	
	
	moview_review_vector = vectorizer.transform(movie_reviews_array)
	
	print(clf.predict(moview_review_vector))
	m=(clf.predict(moview_review_vector))
	if m==0:
		msg="this is the negative review"
	if m==1:
		msg="this is the positive review"
	
	return render_template('result.html',msg = msg, msg2=msg2)
			

if __name__=='__main__':
	app.run(debug=True)

	
	
	
	
	
	
	
	