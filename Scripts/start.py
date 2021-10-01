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
from dbconnect import connection
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g, make_response, send_file
from functools import wraps
import MySQLdb
from MySQLdb import escape_string as thwart
import json
import datetime
from datetime import datetime,timedelta
from time import mktime
import os
import time
import urllib2
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from dbconnect import connection
import gc
import urllib
import re
import smtplib
from add import addstock
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
#import BeautifulSoup
import time
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
from newsif import new
from functools import wraps
from try4 import reco


app = Flask(__name__, static_url_path = "/tmp", static_folder = "tmp")

if __name__ == "__main__":
    app.secret_key = 'super secret key'

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [{'User-agent','Mozilla/5.0'}]


def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			return render_template("mainpage.html")
	return wrap
	


	
@app.route("/logout/")
@login_required
def logout():
	c,conn = connection()
	c.execute("DELETE FROM temp_user where id='1'")
	conn.commit()
	session.clear()
	return redirect(url_for("main"))
	


		
@app.route("/login/", methods = ['GET','POST'])
def login():
	error = ''
	try:
		c,conn = connection()
		if request.method == "POST":
			
			
			data = c.execute("select * from users where username = (%s)", [thwart(request.form['username'])])
			data = c.fetchone()
			
			if (request.form['password'])==data[2]:
				session['logged_in'] = True
				session['username'] = request.form['username']
				
			if (session['logged_in'] == True):
				c.execute("INSERT INTO temp_user (username,id) VALUES (%s,'1')",
                            [thwart(request.form['username'])])
				conn.commit()
			
				
				
				return redirect(url_for("mypage"))
			else:
				error = "Invalid credentials,try again."
				
			gc.collect()	
			return render_template("mainpage.html", error = error)

	except Exception as e:
		
		error = "Invalid credentials,try again."
	return render_template("login.html", error = error)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the <a href="/about/tos" target="blank">Terms of Service</a> and <a href="/about/privacy-policy" target="blank">Privacy Notice</a> (updated Jan 22, 2015)', [validators.Required()])
    

@app.route("/mypage")
def mypage():
	return redirect(url_for("main"))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    try:
        c,conn = connection()
        error = None
        if request.method == 'POST':
            try:
                data = c.execute("SELECT * FROM users WHERE username = (%s)",
                        thwart(request.form['username']))
                data = c.fetchone()[2]

                if sha256_crypt.verify(request.form['password'], data):
                    #session['logged_in'] = True
                    session['username'] = request.form['username']
                    flash('You are now logged in.')
                    return render_template("mainpage.html")
            except Exception, e:
                flash("What are you doing?")


            try:
                
                if request.method == 'POST' and form.validate():

                    username = form.username.data
                    email = form.email.data

                    password = form.password.data
                    c,conn = connection()

                    x = c.execute("SELECT * FROM users WHERE username = (%s)", (thwart(username),))

                    if int(x) > 0:
                        flash("That username is already taken, please choose another")
                        return render_template('register.html', form=form)

                    else:
                        c.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                            (thwart(username), thwart(password), thwart(email)))
                        conn.commit()
                        flash('Thanks for registering')
                        c.close()
                        conn.close()
                        gc.collect()
                        #session['logged_in'] = True
                        session['username'] = username
                        return redirect(url_for('main'))

            except Exception as e:
                return(e)
  
            else:
                flash('Invalid credentials. Try again')
        gc.collect()
        return render_template("register.html", error=error, form=form, page_type = "register")
    except Exception, e:
        return(e)




class AddStockForm(Form):
	stockname = TextField('Stock Name', [validators.Length(min=2, max=20)])
	quantity = TextField('Quantity', [validators.Length(min=1, max=50)])
	stockdate = TextField('Investment Date', [validators.Length(min=6, max=10)])
	userprice = TextField('Investment Price', [validators.Length(min=2, max=10)])
	
class calculateform(Form):
	rupees = TextField('Rupees', [validators.Length(min=2, max=20)])
	currency = TextField('currency', [validators.Length(min=2, max=20)])
    
	
	

@app.route('/', methods=['GET', 'POST'])

def main():
	
	page='http://www.moneycontrol.com/mccode/currencies/'
	sourcecode = opener.open(page).read()  
	var=184    
	bp = re.findall(r'<td class="bgylw" align="right">(.*?)</td>',sourcecode)
	ob=list(bp)
	
	bp1 = ob[12]
	bp2 = ob[13]
	ausd = float(bp1)
	yen = float(bp2)
		
	page='http://www.moneycontrol.com/currency/mcx-gbpinr-price.html'
	sourcecode = opener.open(page).read()  
	var=184    
	bp = re.findall(r'<span class="gr_30">(.*?)</span>',sourcecode)
	ob=list(bp)
	bp1 = ob[0]
	pound = float(bp1)
	
	
	page='https://in.finance.yahoo.com/'
	sourcecode = opener.open(page).read()  
	var=184    
	price = re.findall(r'<span id="yfs_(.*?)_(.*?)bsesn" class="l84">(.*?)</span>',sourcecode)
	ob= list(price)
	for elem in ob:
            z = elem[2]
	flash (z)
	niftyprice = re.findall(r'<span id="yfs_(.*?)_(.*?)nsei" class="l84">(.*?)</span>',sourcecode)
	ob= list(niftyprice)
	for elem in ob:
            z = elem[2]
	flash (z)
	
	europrice = re.findall(r'<span id="yfs_(.*?)_eurinr(.*?)x" class="l84">(.*?)</span>',sourcecode)
	ob= list(europrice)
	for elem in ob:
		z = elem[2]
		euro = float(elem[2])
            
			
	flash (z)
	
	oilprice = re.findall(r'<span id="yfs_(.*?)_clj16(.*?)nym" class="l84">(.*?)</span>',sourcecode)
	ob= list(oilprice)
	for elem in ob:
            z = elem[2]
	flash (z)
	var='http://economictimes.indiatimes.com/'
	dollarprice = re.findall(r'<span id="yfs_(.*?)_usdinr(.*?)x" class="l84">(.*?)</span>',sourcecode)
	ob= list(dollarprice)
	for elem in ob:
		z = elem[2]
		dollar = float(elem[2])
            
			
	flash (z)
	
	activestocks = 'http://www.moneycontrol.com/stocks/marketstats/bsemact1/'
	sc4 = opener.open(activestocks).read()
	link4 = re.findall('<b>(.*?)</b>',sc4)
	e = 1
	k = 1
	for lin in link4:
		if e>6:
			if k<6:
				flash (lin)
				k = k+1
				e = e+1
		e = e+1
	
	page3 = 'http://www.moneycontrol.com/stocks/marketstats/bsegainer/'
	
	
	sourcecode3 = opener.open(page3).read()
	link = re.findall('<b>(.*?)</b>',sourcecode3)
	e = 1
	k = 1
	for lin in link:
		if e>6:
			if k<6:
				flash (lin)
				k = k+1
				e = e+1
		e = e+1
	
	page1 = 'http://www.moneycontrol.com/stocks/marketstats/bseloser/'
	sc = opener.open(page1).read()
	link1 = re.findall('<b>(.*?)</b>',sc)
	e = 1
	k = 1
	for lin in link1:
		if e>=6:
			if k<6:
				flash (lin)
				k = k+1
				e = e+1
		e = e+1
		

	form = calculateform(request.form)
	c,conn = connection()

	if request.method == 'POST':
		
		if request.form['submit'] == 'My Portfolio':	
			return redirect(url_for('firstpage')) # do something
		elif request.form['submit'] == 'News':
			return redirect(url_for('news'))
		elif request.form['submit'] == 'Home':
			return redirect(url_for('main'))
		elif request.form['submit'] == 'Commodities':
			return redirect(url_for('commodities'))
		elif request.form['submit'] == 'Prediction':
			return redirect(url_for('prediction')) # do something else
		elif request.form['submit'] == 'Recommendation':			
			return redirect(url_for('recommendation')) 
		elif request.form['submit'] == 'Calculate':
			c,conn = connection()
			rupees = form.rupees.data
			currency = form.currency.data
			
			if currency == "US Dollar":
				value = float(rupees)/dollar
				flash (value)
			if currency == "Euro":
				value = float(rupees)/euro
				
				flash (value)
			if currency == "British Pound":
				value = float(rupees)/pound
				
				flash (value)
			if currency == "Australian Dollar":
				value = float(rupees)/ausd
				
				flash (value)
			if currency == "Japanese Yen":
				value = float(rupees)/yen
				
				flash (value)
			
			
			return render_template("mainpage.html", error=None, form=form, page_type = "home", text ="hiiii\nhoooo")
		else:
			pass
		
	
	return render_template("mainpage.html", error=None, form=form, page_type = "home", text ="hiiii\nhoooo")
	
	
	
@app.route('/portfolio/', methods=['GET', 'POST'])
def portfolio(): 
	form=AddStockForm(request.form)
	if request.method == 'POST':
		add=addstock()
		
		return (add)
	
	return render_template("addstock.html", error=None, form=form, page_type = "addstock")
	
class AddP(Form):
    stockname = TextField('Stock Sector', [validators.Length(min=1, max=20)])
	
@app.route('/prediction/', methods=['GET', 'POST'])
def prediction(): 
	form = AddP(request.form)
	c,conn = connection()
	error = None
	if request.method == 'POST':
		if request.method == 'POST' and form.validate():
				stockname = form.stockname.data
				flash (stockname)
				x = c.execute("SELECT stocksite FROM stocksymbol WHERE stockname = (%s)", (thwart(stockname),))
				temp = c.fetchall ()
				ans = list(temp[0])
				page=ans[0]
				#return page
				var='http://www.moneycontrol.com'
				sourcecode = opener.open(page).read()      

				text_file = open("save.txt", "w")
				links = re.findall(r'<a href=(.*?) class="g_14bl">',sourcecode)
				i = 0
				for link in links:
					if i<5:
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
				t.close()
				c1 = 0
				c0 = 0
				cls = Classifier(classname="weka.classifiers.trees.RandomForest")
				cls.build_classifier(filtered1)
				for index, inst in enumerate(filtered2):
					pred = cls.classify_instance(inst)
					if pred == 1.0:
						c1=c1+1
						
					else:
						c0=c0+1
						
					dist = cls.distribution_for_instance(inst)
				
				
				if c1 <= c0:
					flash ("DECREASE")
					print str("DECREASE")
					return render_template("pred.html")
				else:
					flash ("INCREASE")
					print str("INCREASE")
					return render_template("pred.html")
					
					
				evl = Evaluation(iris_inc)

							
								
						
				
				
	
	
			
	return render_template("Prediction.html", error=error, form=form, page_type = "home", text ="hiiii\nhoooo")

	
@app.route('/firstpage/', methods=['GET', 'POST'])
def firstpage():
	form = AddStockForm(request.form)
	c,conn = connection()

	if request.method == 'POST':
		
		if request.form['submit'] == 'Add Stock':	
			return redirect(url_for('portfolio')) # do something
		elif request.form['submit'] == 'Sell Stock':
			return redirect(url_for("sell"))
		elif request.form['submit'] == 'My Stocks':
			return redirect(url_for("home"))
		elif request.form['submit'] == 'Threshold':
			return redirect(url_for("threshold"))
		elif request.form['submit'] == 'Wish List':
			return ("hellllooooooooooo")
	
	
	form = AddStockForm(request.form)
	c,conn = connection()
	y = c.execute("SELECT userprice,quantity FROM addstock,temp_user WHERE temp_user.username=addstock.username")
	data = c.fetchall()
	sum=0
	y = list(data)
	for elem in y:
		z=list(elem)
		a = float(z[0])*float(z[1])
		sum = sum+a
	flash (sum)
	y = c.execute("SELECT stocksymbol, quantity FROM addstock, stocksymbol,temp_user WHERE stocksymbol.stockname = addstock.stockname AND temp_user.username=addstock.username")
	data = c.fetchall ()
	ob = list(data)
	cursum = 0
	for elem in ob:
		l = list(elem)
		print l[0]
		url = "http://finance.yahoo.com/q?s=" +l[0] +"&ql=1"
		htmlfile = urllib.urlopen(url)
		htmltext = htmlfile.read()
		regex = '<span id="yfs_l84_'+l[0]+'">(.+?)</span>'
		pattern = re.compile(regex)
		price = re.findall(pattern, htmltext)
		d = price[0]
		if ',' in d:
			d = price[0].replace(',','')
		d = float(d)*float(l[1])
		
		cursum = cursum + d
	res = cursum - sum
	print (res)
	flash (res)
	
	
	c,conn = connection()
	y = c.execute("SELECT * FROM threshold")
	if y>0:
		p = c.execute("SELECT stocksymbol,stocksymbol.stockname FROM threshold, stocksymbol,temp_user WHERE threshold.stockname = stocksymbol.stockname AND temp_user.username=threshold.username")
		p = c.fetchall()
		ob = list(p)
		for elem in ob:
			l = list(elem)
			a= l[1]
			url = "http://finance.yahoo.com/q?s=" +l[0] +"&ql=1"
			htmlfile = urllib.urlopen(url)
			htmltext = htmlfile.read()
			regex = '<span id="yfs_l84_'+l[0]+'">(.+?)</span>'
			pattern = re.compile(regex)
			price = re.findall(pattern, htmltext)
			d = price[0]
			if ',' in d:
				d = price[0].replace(',','')
				d = float(d)
			fin = float(d)
			
			mn = c.execute("SELECT min FROM threshold WHERE stockname=(%s)",(thwart(l[1]),))
			cd = c.fetchall()
			cd1 = list(cd)
			min = list(cd1[0])
			min1 = float(min[0])
			op = c.execute("SELECT max FROM threshold WHERE stockname=(%s)",(thwart(l[1]),))
			op = c.fetchall()
			op1 = list(op)
			max = list(op1[0])
			
			max1 = float(max[0])
			print max1
			
			
			if fin < min1:
				flash (l[1]+" Crossed minimum value")
			elif fin > max1:
				flash (l[1]+" Crossed maximum value")
			else:
				print l[1]
				flash (l[1]+" With in max and min threshold")
	else:
		flash ("No Threshold Set")
			
	
		
	return render_template("portfolio.html", form=form, error=None)
		
class thresh(Form):
	minimum = TextField('Stock Sector', [validators.Length(min=1, max=20)])
	maximum = TextField('Stock Sector', [validators.Length(min=1, max=20)])
	stockname = TextField('Stock Sector', [validators.Length(min=1, max=20)])
class SellStockForm(Form):
	stockname = TextField('Stock Name', [validators.Length(min=1, max=20)])	
	
@app.route('/sell/', methods=['GET', 'POST'])
def sell():
	form = SellStockForm(request.form)
	c,conn = connection()
	if request.method == "POST":
		
		username = c.execute("SELECT username FROM temp_user WHERE id=1")
		username = c.fetchall()
		user = list(username[0])
		data = form.stockname.data
		x =c.execute("SELECT stockname FROM addstock WHERE stockname=(%s) AND username=(%s)",(thwart(data),user[0])) 
		if x==0:
			flash (data+" not present in your portfolio")
			return redirect(url_for("sell"))
		else:
		
			x =c.execute("DELETE FROM addstock WHERE stockname=(%s) AND username=(%s)",(thwart(data),user[0]))
			x = c.fetchall()
			conn.commit()
			flash (data+" stock deleted from Portfolio")
	return render_template("sell.html",form=form)
		
		
		
	
@app.route('/threshold/', methods=['GET', 'POST'])
def threshold():
	form = thresh(request.form)
	c,conn = connection()
	if request.method=='POST':
		username = c.execute("SELECT username FROM temp_user WHERE id=1")
		username = c.fetchall()
		user = list(username[0])
		stockname = form.stockname.data
		min = form.minimum.data
		max = form.maximum.data
		x =c.execute("SELECT stockname FROM threshold WHERE stockname=(%s)",(thwart(stockname),)) 
		if x>0:
			return redirect(url_for("threshold"))
		else:
			y = c.execute("INSERT INTO threshold (stockname, min, max,username) VALUES (%s, %s, %s,%s)",
                            (thwart(stockname),thwart(min),thwart(max),user[0]))
			conn.commit()
			return redirect(url_for("threshold"))
	x = c.execute("SELECT stockname,min,max FROM threshold,temp_user WHERE temp_user.username=threshold.username")
	data = c.fetchall()
	l = list(data)
	for elem in l:
		r = list(elem)
		flash (r[0])
		flash (r[1])
		flash (r[2])
	
	return render_template("threshold.html",form=form,error=None)
	

class AddS(Form):
    sector = TextField('Stock Sector', [validators.Length(min=1, max=20)])

@app.route('/sectors/', methods=['GET', 'POST'])
def sectors():
	form = AddS(request.form)
	c,conn = connection()
	error = None
	
	if request.method == 'POST':
		if request.method == 'POST' and form.validate():
			sector = form.sector.data
			c,conn = connection()
			x = c.execute("SELECT stockname,stocksite FROM stocksymbol WHERE sector = (%s)", (thwart(sector),))
			data = c.fetchall ()
			
			ob = list(data)
			for elem in ob:
				page = elem[1]
				var='http://www.moneycontrol.com'
				sourcecode = opener.open(page).read()      

				text_file = open("save.txt", "w")
				links = re.findall(r'<a href=(.*?) class="g_14bl">',sourcecode)
				i = 0
				for link in links:
					if i<5:
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
				t.close()
				c1 = 0
				c0 = 0
				cls = Classifier(classname="weka.classifiers.trees.RandomForest")
				cls.build_classifier(filtered1)
				for index, inst in enumerate(filtered2):
					pred = cls.classify_instance(inst)
					if pred == 1.0:
						c1=c1+1
						
					else:
						c0=c0+1
						
					dist = cls.distribution_for_instance(inst)
				
				
				
				if c1 >= c0:
					flash (elem[0])
					flash ("INCREASE")
					
				else:
					flash (elem[0])
					flash ("DECREASE")
					
		return render_template("sectorpred.html",form=form)
					
					
				

							
								
			
	return ("done")
	
@app.route('/recommendation/', methods=['GET', 'POST'])
def recommendation(): 
	form = AddS(request.form)
	c,conn = connection()
	error = None
	
	if request.method == 'POST':
		if request.method == 'POST' and form.validate():
			sector = form.sector.data
			c,conn = connection()
			x = c.execute("SELECT stockname,volumesite FROM stocksymbol WHERE sector = (%s)", (thwart(sector),))
			data = c.fetchall ()
			
			ob = list(data)
			data = []
			for elem1 in ob:
				rem = c.execute("SELECT stockname FROM addstock WHERE stockname = (%s)", (thwart(elem1[0]),))
				
				rem1 = c.fetchall()
				if rem>0:
					m = list(rem1)
					
					lo = list(rem1[0])
					if lo[0]==elem1[0]:
						ob.remove(elem1)
	
			for elem in ob:
				z = list(elem)
				page=z[1]
				sourcecode = opener.open(page).read()      
				volume = re.findall(r'<p id="b_total_buy_qty" class="FR">(.*?)</p>',sourcecode)
				z[1]=volume[0]
				data.append(z)
			print str(data)
			new_list = list()
			while data:
				a = data[0]
				
				minimum = a[1]  # arbitrary number in list 
				for x in data:
					if x < minimum:
						minimum = x
				new_list.append(minimum)
				data.remove(minimum) 
			print str(new_list)
			for elem in new_list:
				l=elem[0]
				print l
				x = c.execute("SELECT stocksite FROM stocksymbol WHERE stockname = (%s)", (thwart(l),))
				temp = c.fetchall ()
				ans = list(temp[0])
				page=ans[0]
				#return page
				var='http://www.moneycontrol.com'
				sourcecode = opener.open(page).read()      

				text_file = open("save.txt", "w")
				links = re.findall(r'<a href=(.*?) class="g_14bl">',sourcecode)
				i = 0
				for link in links:
					if i<5:
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
				t.close()
				c1 = 0
				c0 = 0
				cls = Classifier(classname="weka.classifiers.trees.RandomForest")
				cls.build_classifier(filtered1)
				for index, inst in enumerate(filtered2):
					pred = cls.classify_instance(inst)
					if pred == 1.0:
						c1=c1+1
						
					else:
						c0=c0+1
						
					dist = cls.distribution_for_instance(inst)
				
				
				
				if c1 < c0:
					print (elem[0])
					
				else:
					flash (elem[0])
					return render_template("Recommendation.html")
					
					
					
				

							
								
			flash ("No Recommended Stocks")	
			return render_template("Recommendation.html")
				
				
	
	

	return render_template("Reco.html", error=error, form=form, page_type = "home", text ="hiiii\nhoooo")
	
	
	
@app.route('/home/', methods=['GET', 'POST'])
def home():
    form = AddStockForm(request.form)
    try:
		c,conn = connection()
		error = None
		stockname = form.stockname.data
		quantity = form.quantity.data
		stockdate = form.stockdate.data
		userprice = form.userprice.data
		c,conn = connection()
		y = c.execute("SELECT stocksymbol FROM addstock, stocksymbol,temp_user WHERE stocksymbol.stockname = addstock.stockname AND temp_user.username=addstock.username")
		data = c.fetchall ()
		ob = list(data)
		for elem in ob:
			z = list(elem)
			url = "http://finance.yahoo.com/q?s=" +z[0] +"&ql=1"
			htmlfile = urllib.urlopen(url)
			htmltext = htmlfile.read()
			regex = '<span id="yfs_l84_'+z[0]+'">(.+?)</span>'
			pattern = re.compile(regex)
			price = re.findall(pattern, htmltext)
			a = c.execute("SELECT stockname FROM stocksymbol WHERE stocksymbol = (%s)", (thwart(z[0]),))
			b = c.fetchall ()
			ab = list(b)
			abc = list(ab[0])
			s = c.execute("SELECT stockname FROM addstock WHERE stockname = (%s)", (thwart(abc[0]),))
			r = c.fetchall()
			l = list(r[0])
			flash (l[0])
			s = c.execute("SELECT quantity FROM addstock WHERE stockname = (%s)", (thwart(abc[0]),))
			r = c.fetchall()
			l = list(r[0])
			flash (l[0])
			s = c.execute("SELECT stockdate FROM addstock WHERE stockname = (%s)", (thwart(abc[0]),))
			r = c.fetchall()
			l = list(r[0])
			flash (l[0])
			s = c.execute("SELECT userprice FROM addstock WHERE stockname = (%s)", (thwart(abc[0]),))
			r = c.fetchall()
			l = list(r[0])
			flash (l[0])
			flash (price[0])
			xy=l[0].replace('\'','')
			xy1 = price[0]
			if ',' in xy1:
				xy1 = xy1.replace(',','')
			
			up = float(xy)
			cp = float(xy1)
			gl = cp-up
			flash (gl)
		return render_template("addedstock.html", error=error, form=form, page_type = "home", text ="hiiii\nhoooo")   
        
                    
    except Exception as e:
                return(str(e))

            
    gc.collect()


class comm(Form):
    com = TextField('COMMODITY', [validators.Length(min=1, max=20)])
    type = TextField('TYPE', [validators.Length(min=1, max=20)])
    quantity = TextField('QUANTITY', [validators.Length(min=1, max=20)])




@app.route('/commodities/', methods=['GET', 'POST'])
def commodities():
	page='http://economictimes.indiatimes.com/commoditysummary/symbol-GOLD.cms'
	sourcecode = opener.open(page).read()  
	var=184    
	goldprice = re.findall(r'<span class="commodityPrice">(.*?)</span>',sourcecode)
	ob=list(goldprice)
	for elem in ob:
            z = elem
	flash (z)

	
	page='http://economictimes.indiatimes.com/commoditysummary/symbol-SILVER.cms'
	sourcecode = opener.open(page).read()  
	var=184    
	silverprice = re.findall(r'<span class="commodityPrice">(.*?)</span>',sourcecode)
	ob=list(silverprice)
	for elem in ob:
            z = elem
	flash (z)
	
	page='http://economictimes.indiatimes.com/commoditysummary/symbol-CRUDEOIL.cms'
	sourcecode = opener.open(page).read()  
	var=184    
	crudeprice = re.findall(r'<span class="commodityPrice">(.*?)</span>',sourcecode)
	ob=list(crudeprice)
	for elem in ob:
            z = elem
	flash (z)
	
	page='http://economictimes.indiatimes.com/commoditysummary/symbol-NATURALGAS.cms'
	sourcecode = opener.open(page).read()  
	var=184    
	naturalgasprice = re.findall(r'<span class="commodityPrice">(.*?)</span>',sourcecode)
	ob=list(naturalgasprice)
	for elem in ob:
            z = elem
	flash (z)
	
	page='http://economictimes.indiatimes.com/commoditysummary/symbol-COPPER.cms'
	sourcecode = opener.open(page).read()  
	var=184    
	copperprice = re.findall(r'<span class="commodityPrice">(.*?)</span>',sourcecode)
	ob=list(copperprice)
	for elem in ob:
            z = elem
	flash (z)
	
	page='http://economictimes.indiatimes.com/commoditysummary/symbol-ALUMINIUM.cms'
	sourcecode = opener.open(page).read()  
	var=184    
	aluminiumprice = re.findall(r'<span class="commodityPrice">(.*?)</span>',sourcecode)
	ob=list(aluminiumprice)
	for elem in ob:
            z = elem
	flash (z)
	
	page='http://economictimes.indiatimes.com/commoditysummary/symbol-NICKEL.cms'
	sourcecode = opener.open(page).read()  
	var=184    
	nickelprice = re.findall(r'<span class="commodityPrice">(.*?)</span>',sourcecode)
	ob=list(nickelprice)
	for elem in ob:
            z = elem
	flash (z)
	
	page='http://economictimes.indiatimes.com/commoditysummary/symbol-LEAD.cms'
	sourcecode = opener.open(page).read()  
	var=184    
	leadprice = re.findall(r'<span class="commodityPrice">(.*?)</span>',sourcecode)
	ob=list(leadprice)
	for elem in ob:
            z = elem
	flash (z)

	
	
	
	   
	
	
	

	return render_template("commodities.html", error=None, page_type = "home", text ="hiiii\nhoooo")
	
	
@app.route('/news/', methods=['GET', 'POST'])
def news(): 
	page = 'http://www.moneycontrol.com/news/'
	var = 'http://www.moneycontrol.com'
	var1='http://economictimes.indiatimes.com' 
	file = open("templates/new.html","w")
	sourcecode = opener.open(page).read()
	title = re.findall('<a class="bd18_open" href=".*?" title="(.*?)"',sourcecode)
	links = re.findall('<a class="bd18_open" href="(.*?)"',sourcecode)
	
	reco = 'http://economictimes.indiatimes.com/markets/stocks/recos'
	source = opener.open(reco).read()
	linkreco = re.findall('<a href="(.*?)"',source)
	titlereco=re.findall('a href=".*?">(.*?)</a>',source)
	
	page2 = 'http://economictimes.indiatimes.com/markets/stocks/announcements'
	var2 ='http://economictimes.indiatimes.com'
 
	file = open("templates/new.html","w")
	sourcecode2 = opener.open(page2).read()
	linksannounce = re.findall('<a href="(.*?)"',sourcecode2)
	titleannounce = re.findall('<h3><a href=".*?">(.*?)</a></h3>',sourcecode2)
	
	page3 = 'http://economictimes.indiatimes.com/markets/stocks/earnings'
	var3 ='http://economictimes.indiatimes.com'
 
	file = open("templates/new.html","w")
	sourcecode3 = opener.open(page3).read()
	linksearning = re.findall('<a href="(.*?)"',sourcecode3)
	titleearning = re.findall('<h3><a href=".*?">(.*?)</a></h3>',sourcecode3)
	
	ab=[]
	for l in linkreco:
		if '.cms' in l:
			if '/recos/' in l:
				if not '/articlelist/' in l:
					ab.append(l)


	for x in ab:
		titlereco=re.findall('<h3><a href=.*?>(.*?)</a></h3>',source)

		
	file.write(" {% block header %}\n<head>\n<title>Portfolio</title>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<link rel=\"stylesheet\" href=\"http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css\">\n<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js\"></script>\n<script src=\"http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js\"></script>\n</head>\n{% block body %}\n<div class=\"text-center\">\n<nav class=\"navbar navbar-default\">\n<div class=\"container-fluid\">\n<ul class=\"nav navbar-nav\">\n<li ><a href=\"/register/\">Sign In</a></li>\n<li><a href=\"/login/\">Login</a></li>\n</div>\n</nav>\n<h1>Trader's View</h1>\n<form method=post action=\"/\">\n<div class=\"btn-group\">\n<input type=\"submit\" class=\"btn btn-info\" value=\"Home\" name=\"submit\">\n<input type=\"submit\" class=\"btn btn-info\" value=\"News\" name=\"submit\">\n<input type=\"submit\" class=\"btn btn-info\" value=\"My Portfolio\" name=\"submit\">\n<input type=\"submit\" class=\"btn btn-info\" value=\"Commodities\" name=\"submit\">\n<input type=\"submit\" class=\"btn btn-info\" value=\"Prediction\" name=\"submit\">\n<input type=\"submit\" class=\"btn btn-info\" value=\"Recommendation\" name=\"submit\">\n<input type=\"submit\" class=\"btn btn-info\" value=\"About Us\" name=\"submit\">\n<input type=\"submit\" class=\"btn btn-info\" value=\"FAQ's\" name=\"submit\">\n<input type=\"submit\" class=\"btn btn-info\" value=\"Contact Us\" name=\"submit\">\n</div>\n<div class=\"container\">\n<h2>Stock News</h2>\n<table class=\"table\">\n<thead><th>\n<table class=\"table\">\n<thead>\n<tr>\n<th>Business News</th>\n</tr>\n</thead>\n<tbody>\n<tr>")
	i=0
	for link in links:
		if i<6:
			file.write("\n<td>\n")

			file.write("<a href = \"")
			a = var+link
			b = a.decode('utf-8')
			file.write(a+"\"><p>")
			
			file.write(title[i])
			
			file.write("</p></a>\n</td>\n")
			file.write("\n<tr></tr>\n")
		i=i+1
	i=1	
	file.write("</tr>\n</tbody>\n</table>\n</th>\n")
	
	file.write("<th>\n<table class=\"table\">\n<thead>\n<tr><th>Recommendations</th>\n</tr>\n</thead>\n<tbody>\n<tr>")	
	xyz=0
	e =0
	for link in ab:
		if i%2==0:
			if e<6:
				file.write("\n<td>\n")

				file.write("<a href = \"")
				a = var1+link
				b = a.decode('utf-8')
				file.write(a+"\"><p>")
				
				file.write(titlereco[xyz])
				
				file.write("</p></a>\n</td>\n")
				file.write("\n<tr></tr>\n")
				xyz=xyz+1
			e=e+1
		i=i+1
	file.write("</tr>\n</tbody>\n</table>\n</th>\n")
	
	file.write("<tr><th>\n<table class=\"table\">\n<thead>\n<tr><th>Announcements</th>\n</tr>\n</thead>\n<tbody>\n<tr>")
	i=1
	oo=0
	for link in linksannounce:
		if i<9:
			if '.cms' in link:
				if '/announcements/' in link:
					if not '/articlelist/' in link:
						file.write("\n<td>\n")

						file.write("<a href = \"")
						a = var2+link
						b = a.decode('utf-8')
						file.write(a+"\"><p>")
						
						file.write(titleannounce[oo])
						
						file.write("</p></a>\n</td>\n")
						file.write("\n<tr></tr>\n")
						i=i+1
						oo=oo+1
		
	
	file.write("</tr>\n</tbody>\n</table>\n</th>")
	
	file.write("<th>\n<table class=\"table\">\n<thead>\n<tr><th>Earnings</th>\n</thead>\n<tbody>\n<tr>")
	i=1
	oo=0
	for link in linksearning:
		if i<9:
			if '.cms' in link:
				if '/earnings/' in link:
					if not '/articlelist/' in link:
						file.write("\n<td>\n")

						file.write("<a href = \"")
						a = var3+link
						b = a.decode('utf-8')
						file.write(a+"\"><p>")
						
						file.write(titleearning[oo])
						
						file.write("</p></a>\n</td>\n")
						file.write("\n<tr></tr>\n")
						i=i+1
						oo=oo+1
	
	file.write("</tr>\n</tbody>\n</table>\n</th>\n</tr>\n</table></div>\n</body>\n</html>\n{% endblock %}\n{% endblock %}")
	
		
	return redirect(url_for('newsfetch'))
		
	return redirect(url_for('newsfetch'))

@app.route('/newsfetch/')
def newsfetch():
	return render_template("new.html")
	
		
if __name__ == "__main__":
    app.debug = True
    app.run()