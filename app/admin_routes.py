from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt, Student, Teacher, Admin, Classes
from app.forms import LoginForm, RegisterFormTeacher, RegisterFormStudent, User, AddNewClass, AssignStudent, \
	UpdateClass, ChooseClass
import flask_login
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.admin_decorator import is_admin
import requests


@app.route('/admin', methods=['GET', 'POST'])
def login_admin():
	form = LoginForm()
	if form.validate_on_submit():
		user = Admin.query.filter_by(email=form.email.data).first()
		if user:
			if user.password == form.password.data:
				flask_login.login_user(user)
				return redirect(url_for('admin_panel'))
			else:
				flash("Not correct")
		else:
			flash("You are not administrator")
			return redirect(url_for('homepage'))
	return render_template('admin.html', title='Login', form=form)


@app.route('/register_teacher', methods=['GET', 'POST'])
@is_admin()
def register_teacher():
	form = RegisterFormTeacher()
	if form.validate_on_submit():
		user = Teacher.query.filter_by(email=form.email.data).first()
		if user:
			flash("This email is already taken")
		else:
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user = Teacher(
				email=form.email.data, password=hashed_password, university=form.university.data, major=form.major.data,
				first_name=form.first_name.data, last_name=form.last_name.data)
			db.session.add(user)
			db.session.commit()
			flash("Account was added", "success")
			return redirect(url_for('admin_panel'))
	return render_template('register_teacher.html', title='Register', form=form)


@app.route('/register_student', methods=['GET', 'POST'])
@is_admin()
def register_student():
	if current_user.is_authenticated:
		form = RegisterFormStudent()
		if form.validate_on_submit():
			user = Student.query.filter_by(email=form.email.data).first()
			if user:
				flash("This email is already taken")
			else:
				hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
				user = Student(email=form.email.data,
				               password=hashed_password,
				               first_name=form.first_name.data,
				               last_name=form.last_name.data,
				               date_of_birth=form.date_of_birth.data,
				               parents_name=form.parents_name.data,
				               parents_phone=form.parents_phone.data)
				db.session.add(user)
				db.session.commit()
				flash("Account was added", "success")
				return redirect(url_for('admin_panel'))
	return render_template('register_student.html', title='Register', form=form)


@app.route('/class_addition', methods=['GET', 'POST'])
@is_admin()
def add_class():
	form = AddNewClass()
	form.teacher_id.choices = [(t.id, (t.first_name + " " + t.last_name)) for t in Teacher.query.all()]
	if form.validate_on_submit():
		classes = Classes(
			teacher_id=form.teacher_id.data, weekday=form.weekday.data, subject=form.subject.data,
			hour=form.hour.data)
		db.session.add(classes)
		db.session.commit()
		flash("Class was added", "success")
		return redirect(url_for('admin_panel'))
	return render_template('class_addition.html', form=form)


@app.route('/class_student', methods=['GET', 'POST'])
@is_admin()
def student_class():
	form = AssignStudent()
	form.student_id.choices = [(t.id, (t.first_name + " " + t.last_name)) for t in Student.query.all()]
	form.classes_id.choices = [(t.id, (t.subject + " " + t.weekday + " " + t.hour)) for t in Classes.query.all()]
	if form.validate_on_submit():
		student1 = Student.query.filter_by(id=form.student_id.data).first()
		class1 = Classes.query.filter_by(id=form.classes_id.data).first()
		student1.classes.append(class1)
		db.session.commit()
		flash("Student was assigned", "success")
		return redirect(url_for('admin_panel'))
	return render_template('class_student.html', form=form)


@app.route('/admin_panel')
@is_admin()
def admin_panel():
	form = ChooseClass()
	form.classes_id.choices = [(t.id, (t.subject + " " + t.weekday + " " + t.hour)) for t in Classes.query.all()]
	return render_template('admin_panel.html', form=form)


@app.route('/class_change', methods=['GET', 'POST'])
@is_admin()
def update_class():
	class_id = request.args.get('class_id')
	classes = Classes.query.filter_by(id=class_id).first()
	teacher = Teacher.query.filter_by(id=classes.teacher_id).first()
	form = UpdateClass()
	form.teacher_id.choices = [(t.id, (t.first_name + " " + t.last_name)) for t in Teacher.query.all()]
	if form.validate_on_submit():
		classes.teacher_id = form.teacher_id.data
		classes.weekday = form.weekday.data
		classes.subject = form.subject.data
		classes.hour = form.hour.data
		db.session.commit()
		flash("Class was changed", "success")
		return redirect(url_for('admin_panel'))
	return render_template('class_change.html', form=form, classes=classes, teacher=teacher)