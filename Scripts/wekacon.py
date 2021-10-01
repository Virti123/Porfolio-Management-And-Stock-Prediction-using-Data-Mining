from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g, make_response, send_file
from functools import wraps
import MySQLdb
from MySQLdb import escape_string as thwart
import datetime
from datetime import datetime,timedelta
from time import mktime
import sys
import time
import urllib2
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from dbconnect import connection
import gc
import urllib
import re
import os
from urllib2 import urlopen
import cookielib
from cookielib import CookieJar
import io
import newspaper
from newspaper import Article
import pickle
from weka.filters import Filter
from weka.classifiers import FilteredClassifier
from weka.classifiers import Evaluation
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g, make_response, send_file
from weka.core.converters import Loader, Saver
from weka.core.classes import Random
import weka.core.jvm as jvm
from weka.classifiers import Classifier
from weka.filters import Filter, MultiFilter, StringToWordVector


app = Flask(__name__)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
	

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [{'User-agent','Mozilla/5.0'}]
	
@app.route('/')
def weka():
	
	page='http://www.moneycontrol.com/company-article/axisbank/news/AB16'
	var='http://www.moneycontrol.com'
	sourcecode = opener.open(page).read()      

	text_file = open("save.txt", "w")
	links = re.findall(r'<a href=(.*?) class="g_14bl">',sourcecode)
	i = 0
	for link in links:
		if i<3:
			if '.html' in link:
					i=i+1
					b = var+link
					text_file.write(b+"\n")
					
							
			else:
				pass
	text_file.close()		
	lista = open("save.txt","r")
	
	apple = 0
	orange = "file_" + str(apple) + ".arff" 
	for line in lista.readlines():
			banana = line

			first_article = Article(url= banana , language='en')
			first_article.download()    
			first_article.parse()
			data = first_article.text
			for l in data:
				if l=="\"":
					data = data.replace("\"","")
			for l in data:
				if l=="'":
					data = data.replace("'","")
			for l in data:
				if l=="?":
					data = data.replace("?","")
			for l in data:
				if l=="\n":
					data = data.replace("\n","")
				
			#print(first_article.text).encode('cp850', errors='replace')

			with io.open(orange, 'a', encoding='utf-8') as f:
					f.write(unicode("'"))
					f.write(data)
					f.writelines(unicode("', ?")+"\n")
					
	
	jvm.start()			
	loader = Loader("weka.core.converters.ArffLoader")
	iris_inc = loader.load_file("io.arff")
	iris_inc.class_is_last()
	loader = Loader("weka.core.converters.ArffLoader")
	iris_inc1 = loader.load_file("file_0.arff")
	iris_inc1.class_is_last()
	s2wv = StringToWordVector(options=["-W", "10", "-L", "-C"])
	s2wv.inputformat(iris_inc)
	filtered1 = s2wv.filter(iris_inc)
	filtered2 = s2wv.filter(iris_inc1)
	os.remove("file_0.arff")
	
	t=open("file_0.arff","w")
	t.write("@relation C__Users_VIRU_Downloads_stock\n\n@attribute text string\n\n@attribute @@class@@ {neg,pos}\n\n@data\n\n")

	c1 = 0
	c0 = 0
	cls = Classifier(classname="weka.classifiers.trees.RandomForest")
	cls.build_classifier(filtered1)
	for index, inst in enumerate(filtered2):
		pred = cls.classify_instance(inst)
		if pred == 1.0:
			print pred
			c1=c1+1
		else:
			print pred
			c0=c0+1
		dist = cls.distribution_for_instance(inst)
	print ("Number of positive instances")
	print (c1)   
	print ("Number of negative instances")
	print (c0)
	if c1 > c0:
		return ("The price will INCREASE")
	else:
		return ("The price will DECREASE")
		
	evl = Evaluation(iris_inc)

				
					
			
				
	jvm.stop()

			
	
	
	
	
	
	return ("x")
	

				
					
			
				

				
				
				
		
			

gc.collect()


if __name__ == "__main__":
    app.debug = True
    app.run()
