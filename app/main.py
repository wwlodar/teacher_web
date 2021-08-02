from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt, Student, Teacher, Admin
from app.forms import LoginForm, RegisterFormTeacher, RegisterFormStudent, User
import flask_login
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.admin_decorator import is_admin


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            flask_login.login_user(user, remember=form.remember.data)
            return redirect(url_for('homepage'))
        else:
            flash("Not correct")
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/admin', methods=['GET', 'POST'])
def login_admin():
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user:
            if user.password == form.password.data:
                flask_login.login_user(user)
                return redirect(url_for('homepage'))
            else:
                flash("Not correct")
        else:
            flash("You are not administrator")
            return redirect(url_for('homepage'))
    return render_template('admin.html', title='Login', form=form)


@app.route('/register_teacher')
@is_admin()
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegisterFormTeacher()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Teacher(email=form.email.data, password=hashed_password, university=form.university.data,
                       subjects=form.subjects.data, first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(user)
        db.session.commit()
        flash("Account was added", "success")
        return redirect(url_for('login_user'))
    return render_template('register_teacher.html', title='Register', form=form)


@app.route('/register_student')
@is_admin()
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegisterFormStudent()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Student(email=form.email.data, password=hashed_password, first_name=form.first_name.data,
                       last_name=form.last_name.data)
        db.session.add(user)
        db.session.commit()
        flash("Account was added", "success")
        return redirect(url_for('login_user'))
    return render_template('register_student.html', title='Register', form=form)
