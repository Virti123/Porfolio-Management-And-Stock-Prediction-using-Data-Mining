from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g, make_response, send_file
from functools import wraps

import datetime
from datetime import datetime,timedelta
from time import mktime
import os
import time
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import gc
app = Flask(__name__)
if __name__ == "__main__":
    app.secret_key = 'super secret key'

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [{'User-agent','Mozilla/5.0'}]
a = 'http://economictimes.indiatimes.com';
var = 'infosys-technologies-ltd'
c = '10960' 
@app.route("/", methods = ['GET','POST'])
def main():
    try:
        page = 'http://economictimes.indiatimes.com/'+var+'/stocks/companyid-'+c+'.cms'
        sourcecode = opener.open(page).read()        
        try:
            text_file = open("Output.txt", "w")
            titles = re.findall(r'<title>(.*?)</title>',sourcecode)
            links = re.findall(r'<a.*?href="(.*?)"',sourcecode)
            for title in titles:
                #print 'THE TITLE IS'
                print(title)
               
            for link in links:
                if '.cms' in link:
                    if not '/articlelist/' in link:
                        if not '/earnings/' in link:
                            #if '/recos/' in link:
                              #  b = a+link
                                #print(b)
                               # linkSource = opener.open(b).read()
                                #content = re.findall(r'<p>(.*?)</p>',linkSource)
                                #for theContent in content:
                                    #print theContent
                                    #if '<a href=' in theContent:
                                        #pass
                               # else:
                                    #text_file = open("Output.txt", "w")
                                    #print 'hiiiii'
                                    #text_file.write(theContent)
                                    #text_file.close()
                                
                            #else:
                                if '/news/' in link:
                                    b = a+link
                                    print(b)
                                    linkSource = opener.open(b).read()
                                    content = re.findall(r'<p>(.*?)</p>',linkSource)
                                    contents = re.findall(r'<div class="Normal">(.*?)</div>',linkSource)
                                    for theContents in contents:
                                        if '<br>' in theContents:
                                            pass
                                        else:
                                            print theContents
                                            text_file.write(theContents)
                                    for theContent in content:
                                        if '<a href=' in theContent or '<meta content="cms.next" name="cmsei">' in theContent or 'Will be displayed' in theContent or 'Will not be displayed' in theContent or 'Your Reason has been Reported to the admin.' in theContent or '<img clas="(.*?)"/>' in theContent or '<meta content="cms.next" name="cmsei"/>' in theContent or '<strong>' in theContent or '</strong>' in theContent:
                                            pass
                                        else:
                                            print theContent
                                            text_file.write(theContent)
                                    
                                                   
                                    
                                    #text_file.close()
                else:
                    pass

        except Exception as e:
            print (e)

        
    except Exception as e:
        print (e)


main()

    


if __name__ == "__main__":
    app.debug = True
    app.run()