from weka.filters import Filter
from weka.classifiers import FilteredClassifier
from weka.classifiers import Evaluation
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g, make_response, send_file
from weka.core.converters import Loader, Saver
from weka.core.classes import Random
import weka.core.jvm as jvm
from weka.classifiers import Classifier


app = Flask(__name__)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
	

	
@app.route('/')
def weka():
	
	
	jvm.start()			
	loader = Loader("weka.core.converters.ArffLoader")
	iris_inc = loader.load_file("io.arff")
	iris_inc.class_is_last()
	remove = Filter(classname="weka.filters.unsupervised.attribute.StringToWordVector")
	cls = Classifier(classname="weka.classifiers.trees.RandomForest")
	fc = FilteredClassifier()
	fc.filter = remove
	fc.classifier = cls
	evl = Evaluation(iris_inc)
	evl.crossvalidate_model(fc, iris_inc, 10, Random(1))
	print(evl.percent_correct)
	print(evl.summary())
	print(evl.class_details())

	
	return unicode(evl.summary())

				
					
			
				
	jvm.stop()



if __name__ == "__main__":
    app.debug = True
    app.run()
