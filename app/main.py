from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt, Student, Teacher, Admin, Classes
from app.forms import LoginForm, RegisterFormTeacher, RegisterFormStudent, User
import flask_login
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import calendar


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flask_login.login_user(user, remember=form.remember.data)
            return redirect(url_for('homepage'))
        else:
            flash("Not correct")
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/teachers')
def teachers_page():
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

@app.route('/profile')
def my_profile():
    if current_user.is_authenticated and current_user == Admin.query.filter_by(email=current_user.email).first():
        return redirect(url_for('admin_panel'))
    return render_template('profile.html')


@app.route('/schedule')
def schedule_page():
    weekdays = Classes.query.all()
    return render_template('schedule.html', weekdays=weekdays)
