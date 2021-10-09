from flask import render_template, request, redirect, Blueprint, url_for
from flask_login import login_user, current_user, logout_user, login_required
from flasktodo.models import Task
from flasktodo import db, bcrypt

main = Blueprint('main', __name__)

@main.route('/')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	else:
		return render_template('welcome.html', title='Welcome')

@main.route('/tasks')
def home():
	tasks = Task.query.filter_by(completed=False, author=current_user).order_by(Task.date_added.desc()).all()
	return render_template('home.html', tasks=tasks)

@main.route('/about')
def about():
	return render_template('about.html', title='About')