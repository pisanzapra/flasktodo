from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flasktodo import db, login_manager # may need to update
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


# import from db.Model
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	# One to many rship. Backref similar to adding another column to the task model. 
	# Lazy argument defines when SQLAlchemy loads the data from the database
	# Upper case on Task b/c we're referencing the class
	tasks = db.relationship('Task', backref='author', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	#telling python not to expect self parameter as an argument
	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	# how our object looks when printed out
	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task_name = db.Column(db.String(100), nullable=False)
	date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	completed = db.Column(db.Boolean, default=False, nullable=False)

	# how our object looks when printed out
	def __repr__(self):
		return f"Task('{self.id}', '{self.task_name}', '{self.date_added}', '{self.completed}')"