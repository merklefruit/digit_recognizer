# Digit Recognizer
A Python implementation of the popular MNIST dataset application of Digit Recognition with Convolutional Neural Networks

This project was made to demonstrate a Python implementation of web inference capability.
The network was trained on the MNIST database in Jupyter Notebook with the Keras library with Tensorflow backend. The recognition error on the test data set is 0.75% after 12 epochs, without hyperparameter tuning. The convolutional neural network I used is an 8-layer Sequential model.

This project is available as a full featured demo here: http://www.digitrecognition.nicolasracchi.com

In this demo there is also a brief explanation of how the neural network works.


## Installation

1. Just cd in the flask_3 folder, activate your virtual environment, and run:


`pip install -r requirements.txt`

`flask run`


## How it works:

The neural network was trained on the MNIST dataset in a Jupyter Notebook in Python, using ADAM, an algorithm for first-order gradient-based optimization of stochastic objective functions, based on adaptive estimates of lower-order moments.
The loss function choosen was categorical crossentropy, since there are 10 classes.
The network itself is an 8 layer sequential model, which has 784 input units (28x28 resolution grayscale images, normalized to values ranging from [-1: 1]). The network structure is as follows:
							
  * 2 Convolutional layers with rectified linear unit activation
  * A Pooling layer to choose the best features of the digits
  * A Dropout layer to improve convergence
  * A Flatten layer since there are too many dimensions and we need only 10 classes
  * A Dense layer, fully connected, to get all relevant data
  * A second Dropout layer
  * A Dense layer with softmax activation to squash the matrix into output probabilities

Using this training method I was able to obtain 99.25% test accuracy after only 12 epochs, without hyperparameter tuning, so there is still room for improvement.
The training process took 16 seconds per epoch on a GRID 520 GPU.

### Preprocessing

When you draw an image in the canvas, you are writing into a 280x280px area. The preprocessing is needed so that the output of the canvas is as similar as possible to the training data, in order to not loose accuracy.
First of all, the image is converted in a base64 string, then its colors are inverted so that the majority of the canvas is black (this makes it easier for the classifier); finally, it is resized to 28x28px, the same as the training data.
