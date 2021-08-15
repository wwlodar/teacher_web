from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt, Student, Teacher, Admin, Classes, User
from app.forms import LoginForm, User, ChangeTeacherForm, ChangeStudentForm
import flask_login
from flask_login import current_user, logout_user, login_required


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


@app.route('/schedule')
def schedule_page():
  classes = Classes.query.all()
  return render_template('schedule.html', classes=classes)


@app.route('/profile')
def my_profile():
  if current_user.is_authenticated and current_user == Admin.query.filter_by(email=current_user.email).first():
    return redirect(url_for('admin_panel'))
  elif current_user == Teacher.query.filter_by(email=current_user.email).first():
    return redirect(url_for('teachers_profile'))
  else:
    return redirect(url_for('students_profile'))


@app.route('/teacher_profile')
@login_required
def teachers_profile():
  teacher_data = Teacher.query.filter_by(email=current_user.email).first()
  classes = [(t.subject + " " + t.weekday + " " + t.hour) for t in Classes.query.filter_by
  (teacher_id=current_user.id).all()]
  return render_template('teacher_profile.html', teacher_data=teacher_data, classes=classes)


@app.route('/change_teacher_form', methods=['GET', 'POST'])
@login_required
def change_teacher_form():
  teacher = Teacher.query.filter_by(email=current_user.email).first()
  form = ChangeTeacherForm()
  if form.validate_on_submit():
      teacher.first_name = form.first_name.data
      teacher.last_name = form.last_name.data
      teacher.major = form.major.data
      teacher.university = form.university.data
      db.session.commit()
      flash("Your information was updated", "success")
      return redirect(url_for('teachers_profile'))
  return render_template('change_teacher_form.html', form=form, teacher=teacher)


@app.route('/student_profile')
@login_required
def students_profile():
  student_data = Student.query.filter_by(email=current_user.email).first()
  classes = [(t.subject + " " + t.weekday + " " + t.hour) for t in student_data.classes.all()]
  return render_template('student_profile.html', student_data=student_data, classes=classes)


@app.route('/change_student_form', methods=['GET', 'POST'])
@login_required
def change_student_form():
  student = Student.query.filter_by(email=current_user.email).first()
  form = ChangeStudentForm()
  if form.validate_on_submit():
      student.first_name = form.first_name.data
      student.last_name = form.last_name.data
      student.date_of_birth = form.date_of_birth.data
      student.parents_name = form.parents_name.data
      student.parents_phone = form.parents_phone.data
      db.session.commit()
      flash("Your information was updated", "success")
      return redirect(url_for('students_profile'))
  return render_template('change_student_form.html', form=form, student=student)
