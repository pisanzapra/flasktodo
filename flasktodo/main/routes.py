from flask import render_template, request, redirect, Blueprint, url_for
from flask_login import login_user, current_user, logout_user, login_required
from flasktodo.models import Task
from flasktodo import db, bcrypt

# url_for, flash, abort

main = Blueprint('main', __name__)

@main.route('/')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	else:
		return render_template('welcome.html', title='Welcome')

@main.route('/tasks')
def home():
	# sets default of page 1
	#page = request.args.get('page', 1, type=int)
	tasks = Task.query.filter_by(completed=False, author=current_user).order_by(Task.date_added.desc()).all()
	#.paginate(page=page, per_page=5)
	return render_template('home.html', tasks=tasks)

@main.route('/about')
def about():
	return render_template('about.html', title='About')