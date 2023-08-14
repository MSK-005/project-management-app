from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import login_required, login_user, logout_user, current_user

from .models import User, Task
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return redirect(url_for('views.home_tasks'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', user=current_user)
    username = request.form.get('username')
    password = request.form.get('password')
    remember_me = request.form.get('remember-me')

    if not username or not password:
        flash('Fill all fields.', category='error')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            if remember_me == 'on':
                login_user(user, remember=True)
            else:
                login_user(user)
            flash('Logged in successfully.', category='success')
            return redirect(url_for('views.home_tasks'))
        else:
            flash('Incorrect password. Try again.', category='error')
            return redirect(url_for('auth.login'))
    else:
        flash('Username not found. Try again.', category='error')
        return redirect(url_for('auth.login'))

@auth.route('new-password', methods=['GET', 'POST'])
@login_required
def set_new_password():
    if request.method == 'GET':
        return render_template('new-password.html', user=current_user)

    new_password = request.form.get('new-password')
    confirm_password = request.form.get('confirm-password')

    if not new_password or not confirm_password:
        flash('Fill all fields.', category='error')
        return redirect(url_for('auth.set_new_password'))
    elif new_password != confirm_password:
        flash('Passwords do not match', category='error')
        return redirect(url_for('auth.set_new_password'))

    user = User.query.filter_by(id=current_user.id).first()

    if check_password_hash(user.password, new_password):
        flash('New password cannot match old password.', category='error')
        return redirect(url_for('auth.set_new_password'))
    
    new_password_hash = generate_password_hash(new_password, method="pbkdf2:sha256", salt_length=8)
    user.password = new_password_hash
    db.session.commit()

    return redirect(url_for('views.home_tasks'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign-up.html', user=current_user)
    
    username = request.form.get('username')
    password = request.form.get('password')
    remember_me = request.form.get('remember-me')

    if not username or not password:
        flash('Fill all fields.', category='error')
        return redirect(url_for('auth.sign-up'))

    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists. Try again.', category='error')
        return redirect(url_for('auth.sign_up'))
    elif len(username) < 4:
        flash('Username must be greater than 3 characters.', category='error')
        return redirect(url_for('auth.sign_up'))
    elif len(password) < 8:
        flash('Password must be greater than 7 characters.', category='error')
        return redirect(url_for('auth.sign_up'))
    else:
        new_user = User(
            password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8),
            username = username,
            date_created = datetime.now()
        )
        db.session.add(new_user)
        db.session.commit()

        if remember_me == 'on':
            login_user(new_user, remember=True)
        
        else:
            login_user(new_user)

        flash('Account created.', category='success')

        return redirect(url_for('views.home_tasks'))

@auth.route('/delete-account', methods=['POST', 'GET'])
@login_required
def delete_account():
    if request.method == 'GET':
        return render_template('delete-account.html', user=current_user)
    
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Fill all fields.', category='error')
        return redirect(url_for('auth.delete_account'))

    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            Task.query.filter_by(user_id=current_user.id).delete()
            User.query.filter_by(id=current_user.id).delete()
            db.session.commit()
            flash('Deleted account successfully', category='success')
            return redirect(url_for('auth.sign_up'))
        else:
            flash('Incorrect password. Try again.', category='error')
            return redirect(url_for('auth.delete_account'))
    else:
        flash('Entered username does not match currently logged in username.', category='error')
        return redirect(url_for('auth.delete_account'))