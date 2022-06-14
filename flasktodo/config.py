import os
from os import environ

class Config:
	SECRET_KEY = os.environ.get('FLASKTODO_SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = environ.get('FLASKTODO_DATABASE_URL').replace("postgres://", "postgresql://", 1) or 'sqlite:///site.db'
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = os.environ.get('MAIL_PORT')
	MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')