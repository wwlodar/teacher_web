from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt
from app.forms import LoginForm, User
import flask_login
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash,check_password_hash

@app.route('/home')
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
    else:
        flash("Please try again")
    return render_template('login.html', title='Login', form=form)


@app.route('/admin')
def admin():
    return render_template("admin.html")
