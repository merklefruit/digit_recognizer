import tensorflow as tf 
from scipy.misc import imread, imresize, imshow
from keras.models import model_from_json
import keras.models
import numpy as np 
import re 
import os
import base64


	# CARICAMENTO MODELLO
def init():
	json_file = open('model/model.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	loaded_model.load_weights("model/model.h5")
	print("Loaded model from disk")

	loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	graph = tf.get_default_graph()

	return loaded_model, graph


	# PREPARAZIONE MODELLO
def convertImage(imgData1):
	imgstring = re.search(b'base64,(.*)',imgData1).group(1)
	with open('output.png', 'wb') as output:
		output.write(base64.b64decode(imgstring))
		print("Binary conversion completed")


def preprocess():
	x = imread('output.png', mode='L')
	x = np.invert(x)
	x = imresize(x, (28, 28))
	x = x.reshape(1, 28, 28, 1)
	print("Preprocessing completed")
	return x