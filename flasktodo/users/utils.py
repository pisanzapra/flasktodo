import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flasktodo import mail
from flask_mail import Message

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='adaandbabs@gmail.com', recipients=[user.email])
	# need _external to get absolute URL
	msg.body = f'''To reset your password, visit the following link:	{url_for('users.reset_token', token=token, _external=True)} 

	If you did not make this request, simply ignore this email and no changes will be made'''
	mail.send(msg)