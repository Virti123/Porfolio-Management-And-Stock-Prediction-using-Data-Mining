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


app = Flask(__name__)

if __name__ == "__main__":
    app.secret_key = 'super secret key'

class AddStockForm(Form):
    stockname = TextField('Stock Name', [validators.Length(min=2, max=20)])
    quantity = TextField('Quantity', [validators.Length(min=1, max=50)])
    stockdate = TextField('Investment Date', [validators.Length(min=6, max=10)])

@app.route('/addstock/', methods=['GET', 'POST'])
def addstock():
	form = AddStockForm(request.form)
	try:
		c,conn = connection()
		error = None
		if request.method == 'POST':
			try:
				if request.method == 'POST' and form.validate():
					stockname = form.stockname.data
					quantity = form.quantity.data
					stockdate = form.stockdate.data
					userprice = form.userprice.data
					c,conn = connection()
					x = c.execute("SELECT * FROM addstock WHERE stockname = (%s)", (thwart(stockname),))
					if int(x) ==-1 :
						flash("That stock is already added")
						return render_template('addstock.html', form=form)
					else:
						c.execute("INSERT INTO addstock (stockname, quantity, stockdate , userprice) VALUES (%s, %s, %s, %s)",
                            (thwart(stockname), thwart(quantity), thwart(stockdate), thwart(userprice)))
						conn.commit()
						c.close()
						conn.close()
						gc.collect()
						return redirect(url_for('home'))
	return render_template("addstock.html", error=error, form=form, page_type = "addstock")
    
						
			
	
	




@app.route('/home/', methods=['GET', 'POST'])
def home():
    form = AddStockForm(request.form)
    try:
        c,conn = connection()
        error = None
        
        
        stockname = form.stockname.data
        quantity = form.quantity.data
        stockdate = form.stockdate.data
        c,conn = connection()

        y = c.execute("SELECT stocksymbol FROM addstock, stocksymbol WHERE stocksymbol.stockname = addstock.stockname")
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
            flash (price[0])
            
            
        return render_template("addedstock.html", error=error, form=form, page_type = "home", text ="hiiii\nhoooo")   
        
                    
    except Exception as e:
                return(str(e))
  
            
    gc.collect()


if __name__ == "__main__":
    app.debug = True
    app.run()