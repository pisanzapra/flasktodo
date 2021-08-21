from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flasktodo.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category= 'info' # set bootstrap class

mail = Mail()

# takes the Config class by default
def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	#imprint Blueprint classes
	from flasktodo.users.routes import users
	# from flaskblog.posts.routes import posts
	from flasktodo.main.routes import main
	# from flaskblog.errors.handlers import errors
	app.register_blueprint(users)
	# app.register_blueprint(posts)
	app.register_blueprint(main)
	# app.register_blueprint(errors)

	return app