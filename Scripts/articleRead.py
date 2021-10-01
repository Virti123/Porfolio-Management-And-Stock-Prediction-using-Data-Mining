from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g, make_response, send_file
import io
import newspaper
from newspaper import Article
import pickle
import os
import smtplib
from pygame
app = Flask(__name__)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
	
@app.route('/')
def weka():
		


	lista = open("save.txt","r")
	print (lista)
	apple = 0
	orange = "file_" + str(apple) + ".arff" 
	for line in lista.readlines():
			banana = line

			first_article = Article(url= banana , language='en')
			first_article.download()    
			first_article.parse()
			data = first_article.text
			#print(first_article.text).encode('cp850', errors='replace')

			with io.open(orange, 'a', encoding='utf-8') as f:
					f.write(unicode("'"))
					f.writelines(first_article.text)
					f.writelines(unicode("', ?")+"\n")
	#os.remove("file_0.arff")
	
	#t=open("file_0.arff","w")
	#t.write("@relation C__Users_VIRU_Downloads_stock\n\n@attribute text string\n\n@attribute @@class@@ {neg,pos}\n\n@data\n\n")
	
					

			
	return ("done")
	
	
	

if __name__ == "__main__":
    app.debug = True
    app.run()

        
