from flask import render_template, flash, redirect, url_for, request 
from app import app, db 
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User 
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html", title='Home Page')


@app.route('/about_me')
def about_me():
	return render_template('about_me.html', title='About me')

@app.route('/recognition')
@login_required
def recognition():
	return render_template('recognition.html', title='Recognition')


# preparo per la chiamata PREDICT
import numpy as np
import os
import sys
sys.path.append(os.path.abspath("./model"))
from load import *

global model, graph
model, graph = init()


@app.route('/predict', methods=['GET', 'POST'])
def predict():
	imgData = request.get_data()
	convertImage(imgData)
	x = preprocess()

	with graph.as_default():
		out = model.predict(x)
		print(out)
		print(np.argmax(out, axis=1))
		response = np.array_str(np.argmax(out, axis=1))
		return response



@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template("login.html", title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)



@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'},
	]
	return render_template('user.html', user=user, posts=posts) 


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.username = form.username.data 
		current_user.about_me = form.about_me.data 
		db.session.commit()
		flash('Your changes have been saved!')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)
















