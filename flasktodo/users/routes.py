from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flasktodo import db, bcrypt
from flasktodo.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flasktodo.models import User
from flasktodo.users.utils import send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		# decode = convert to string r/t bytes
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				next_page = request.args.get('next') # args is a dict. using get method means it'll return none if the method doesn't exist
				# redirect to the next page if it exists. else redirect home
				return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Log in unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Log in', form=form)

@users.route('/logout')
def logout():
	logout_user()
	return render_template('welcome.html', title='Welcome')

@users.route('/account', methods=['GET', 'POST'])
@login_required #need to be logged in to access
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		#if form.picture.data:
			#picture_file = save_picture(form.picture.data)
			#current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	#image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', form=form)
	#image_file=image_file, 

@users.route('/user/<string:username>')
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	# return 404 if none found
	user = User.query.filter_by(username=username).first_or_404()
	# the backslahes allow you to split over multiple lines
	posts = Post.query.filter_by(author=user)\
	.order_by(Post.date_posted.desc())\
	.paginate(page=page, per_page=5)
	return render_template('user_posts.html', posts=posts, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	# Make sure they're logged out
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	# If form is valid grab the email address
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	# Make sure they're logged out
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		# decode = convert to string r/t bytes
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated! You are now able to log in')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)
