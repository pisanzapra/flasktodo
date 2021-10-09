from flask import render_template, url_for, flash, request, redirect, abort, Blueprint
from flask_login import current_user,  login_required
from flasktodo import db
from flasktodo.models import Task
from flasktodo.tasks.forms import TaskForm

# logout_user, login_user

tasks = Blueprint('tasks', __name__)

@tasks.route("/tasks/new", methods=['GET', 'POST'])
@login_required
def new_task():
	form = TaskForm()
	if form.validate_on_submit():
		task = Task(task_name=form.name.data, author=current_user)
		db.session.add(task)
		db.session.commit()
		flash('Your task has been created!', 'success')
		return redirect(url_for('main.home'))
	return render_template('new_task.html', title='New Task', form=form, legend='New Task')

@tasks.route("/task/<int:task_id>/delete", methods=['POST'])
@login_required
def delete_task(task_id):
	task = Task.query.get_or_404(task_id)
	if task.author != current_user:
		abort(403) #forbidden route
	db.session.delete(task)
	db.session.commit()
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('main.home'))

@tasks.route("/task/<int:task_id>/complete", methods=['POST'])
@login_required
def complete_task(task_id):
	task = Task.query.get_or_404(task_id)
	if task.author != current_user:
		abort(403) #forbidden route
	task.completed = True
	db.session.commit()
	flash('Your task has been completed!', 'success')
	return redirect(url_for('main.home'))

@tasks.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
	task = Task.query.get_or_404(task_id)
	if task.author != current_user:
		abort(403) #forbidden route
	form = TaskForm()
	if form.validate_on_submit():
		task.task_name = form.name.data
		db.session.commit()
		flash('Your task has been updated!', 'success')
		return redirect(url_for('main.home'))
	elif request.method == 'GET':
		form.name.data = task.task_name
	return render_template('new_task.html', title='Update Task', form=form, legend='Update Task')



# @tasks.route("/task/<int:task_id>")
# def task(task_id):
# 	task = task.query.get_or_404(task_id)
# 	return render_template('task.html', title=task.title, task=task)

# @tasks.route("/task/<int:task_id>/update", methods=['GET', 'task'])
# @login_required
# def update_task(task_id):
# 	task = task.query.get_or_404(task_id)
# 	if task.author != current_user:
# 		abort(403) #forbidden route
# 	form = taskForm()
# 	if form.validate_on_submit():
# 		task.title = form.title.data
# 		task.content = form.content.data
# 		db.session.commit()
# 		flash('Your task has been updated!', 'success')
# 		return redirect(url_for('tasks.task', task_id=task.id))
# 	elif request.method == 'GET':
# 		form.title.data = task.title
# 		form.content.data = task.content
# 	return render_template('create_task.html', title='Update task', form=form, legend='Update task')

