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
	userprice = TextField('Investment Price', [validators.Length(min=6, max=10)])
	stockname = TextField('Stock Name', [validators.Length(min=2, max=20)])
	quantity = TextField('Quantity', [validators.Length(min=1, max=50)])
	stockdate = TextField('Investment Date', [validators.Length(min=2, max=10)])
	
@app.route('/addstock/', methods=['GET', 'POST'])	
def addstock():
	form = AddStockForm(request.form)
	c,conn=connection()
	if request.method == 'POST':
		if request.method == 'POST' and form.validate():
			stockname = form.stockname.data
			quantity = form.quantity.data
			stockdate = form.stockdate.data
			userprice = form.userprice.data
			c,conn = connection()
			username = c.execute("SELECT username FROM temp_user WHERE id=1")
			username = c.fetchall()
			user = list(username[0])
			x = c.execute("SELECT * FROM addstock WHERE stockname = (%s) AND username = (%s)", (thwart(stockname),user[0],))
			if x>0:
				flash("that stock added")
				return render_template('addstock.html', form=form)
			else:
			
				c.execute("INSERT INTO addstock (stockname, quantity, stockdate , userprice ,username) VALUES (%s, %s, %s, %s, %s)",
								(thwart(stockname), thwart(quantity), thwart(stockdate), thwart(userprice), user[0]))
				conn.commit()
				c.close()
				conn.close()
				gc.collect()
				return redirect(url_for('home'))
			
    
	return render_template("addstock.html", error=None, form=form, page_type = "addstock")

                    
					
					
	
    
if __name__ == "__main__":
    app.debug = True
    app.run()
