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
from functools import wraps
app = Flask(__name__)
if __name__ == "__main__":
    app.secret_key = 'super secret key'
	
	
def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash("You need to login first")
			return redirect(url_for('login'))
	return wrap
	


	
@app.route("/logout/")
@login_required
def logout():
	session.clear()
	flash ("You have been logged out")
	return render_template('mainpage.html')
	


		
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
				flash("You are logged in..!")
				return redirect(url_for("home"))
			else:
				error = "Invalid credentials,try again."
				
			gc.collect()	
			return render_template("login.html", error = error)

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
    

@app.route("/home")
def home():
	return render_template('mainpage.html')


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
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    flash('You are now logged in.')
                    return redirect(url_for('home'))
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
                        session['logged_in'] = True
                        session['username'] = username
                        return redirect(url_for('home'))

            except Exception as e:
                return(e)
  
            else:
                flash('Invalid credentials. Try again')
        gc.collect()
        return render_template("register.html", error=error, form=form, page_type = "register")
    except Exception, e:
        return(e)



if __name__ == "__main__":
    app.debug = True
    app.run()