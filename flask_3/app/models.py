from datetime import datetime
from app import db, login 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

			# la classe UserMixin contiene un po' di cose generiche che vanno bene per le tabelle utenti. come in questo caso.
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	# backref serve per avere a disposizione post.author per dire dinamicamente chi è l'autore di un post.
	about_me = db.Column(db.String(140))

	# repr serve solo ad aiutare python a capire come leggere le info del database
	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


# Quando ho due modelli nel database che sono in relazione uno con l'altro, in questo caso one-to-many, 
# in un modello uso db.relationship() (la parte "many" dell'equazione diciamo) e nell'altro uso db.ForeignKey
# per associare ad esempio l'id dell'autore nella tabella di un post.

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr(self):
		return '<Post {}>'.format(self.body)



@login.user_loader
def load_user(id):
	return User.query.get(int(id))