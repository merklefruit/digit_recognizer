from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_bootstrap import Bootstrap 


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)				# creo l'oggetto database
migrate = Migrate(app, db)		# creo un oggetto che rappresenta il migration engine
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)


from app import routes, models 	# models è per definire la struttura del database


if __name__=='__main__':
	app.run(debug=True)