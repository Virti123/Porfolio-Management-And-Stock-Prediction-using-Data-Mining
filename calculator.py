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

app = Flask(__name__)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
	
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [{'User-agent','Mozilla/5.0'}]

class claculator(Form):
     = TextField('Stock Name', [validators.Length(min=2, max=20)])
    quantity = TextField('Quantity', [validators.Length(min=1, max=50)])
    stockdate = TextField('Investment Date', [validators.Length(min=6, max=10)])

@app.route('/new/')
def new():
	return render_template("calculator.html",form=form)

@app.route('/home/')
def home():
	return render_template("new.html")
			  
if __name__ == "__main__":
    app.debug = True
    app.run()	
			  
