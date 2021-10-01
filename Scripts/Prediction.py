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
	

	
@app.route('/')
def weka():
	
	
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



if __name__ == "__main__":
    app.debug = True
    app.run()
