from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt, Student, Teacher
from app.forms import LoginForm, RegisterForm, User
import flask_login
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash,check_password_hash
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
        if User.query.filter_by(username="Admin"):
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                flask_login.login_user(user, remember=form.remember.data)
                return redirect(url_for('homepage'))
            else:
                flash("Not correct")
        else:
            flash("You are not administartor")
            return redirect(url_for('homepage'))

    return render_template('admin.html', title='Login', form=form)

@app.route('/register')
@is_admin()
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.role.data == "Teacher":
            user = Teacher(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Account was added")
            return redirect(url_for('login_user'))
        else:
            user = Student(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Account was added")
            return redirect(url_for('login_user'))
    return render_template('register.html', title='Register', form=form)
