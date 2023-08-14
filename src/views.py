from flask import Blueprint, render_template, request, flash, redirect, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from .models import Task
from . import db
from .helpers import show_tasks

views = Blueprint('views', __name__)

@views.route('/upcoming', methods=['GET', 'POST'])
@views.route('/inbox', methods=['GET', 'POST'])
@views.route('/today', methods=['GET', 'POST'])
@login_required
def home_tasks():
    rule = str(request.url_rule)

    # If the page is requested by a click of a button from another URL, show the appropriate view
    if request.method == 'GET':
        if 'inbox' in rule:
            tasks = show_tasks(time = None)
            return render_template("inbox.html", user=current_user, tasks=tasks)
        elif 'today' in rule:
            tasks = show_tasks(time = 1)
            return render_template("today.html", user=current_user, tasks=tasks)
        elif 'upcoming' in rule:
            tasks = show_tasks(time = 7)
            return render_template("upcoming.html", user=current_user, tasks=tasks)

    # Validate and create the task
    task_heading = request.form.get('task-heading')
    task_description = request.form.get('task-description')
    task_priority = int(request.form.get('task-priority'))
    task_due_date = request.form.get('task-due-date')

    # if the task heading is empty or the priority is not within the given range, the task creation is invalid
    if not task_heading or task_priority not in range(1, 6):
        flash('Incorrect task creation', category='error')
        return redirect(request.referrer)
    
    # If no date is entered, assign None to the variable, otherwise assign the date the user entered
    if len(task_due_date) == 0:
        task_due_date = None
    else:
        task_due_date = datetime.strptime(task_due_date, '%Y-%m-%d').date()
        task_due_date = datetime.combine(task_due_date, datetime.now().time())

    # Create the new task and enter it in the database
    new_task = Task(heading=task_heading, 
                    description=task_description,
                    priority=task_priority,
                    date_of_creation=datetime.now(),
                    due_date=task_due_date,
                    user_id=current_user.id)
    
    db.session.add(new_task)
    db.session.commit()

    flash('Note created', category='success')
    return redirect(request.referrer)

# Deletes the task by first taking the ID number of the task
@views.route('/delete-task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Note deleted', category='success')
    return redirect(request.referrer)
    

@views.route('/edit-task/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id): 

    # Collects the different values, validates them and edits the task at the given ID number    
    new_task_heading = request.form.get('edit-task-heading--' + str(task_id))
    new_task_priority = int(request.form.get('edit-task-priority--' + str(task_id)))
    new_task_due_date = request.form.get('edit-task-due-date--' + str(task_id))
    new_task_description = request.form.get('edit-task-description--' + str(task_id))
 
    if not new_task_heading or new_task_priority not in range(1, 6):
        flash('Incorrect try at editing the task.', category='error')
        return redirect(request.referrer)
    
    if len(new_task_due_date) == 0:
        new_task_due_date = None
    else:
        new_task_due_date = datetime.strptime(new_task_due_date, '%Y-%m-%d').date()
        new_task_due_date = datetime.combine(new_task_due_date, datetime.now().time())

    task = Task.query.filter_by(id=task_id).first_or_404()
    task.heading = new_task_heading
    task.priority = new_task_priority
    task.due_date = new_task_due_date
    task.description = new_task_description
    db.session.commit()

    flash('Note edited.', category='success')
    return redirect(request.referrer)

@views.route('/settings')
@login_required
def settings():
    return render_template('settings.html', user=current_user)