from flask import render_template, url_for, flash, redirect, Blueprint
from app import app, db, bcrypt
from app.models import Student, User
from app.student.forms import ChangeStudentForm
import flask_login
from flask_login import current_user, logout_user, login_required

student = Blueprint('student', __name__)


@student.route('/student_profile')
@login_required
def students_profile():
  student_data = Student.query.filter_by(email=current_user.email).first()
  classes = [(t.subject + " " + t.weekday + " " + t.hour) for t in student_data.classes.all()]
  return render_template('student_profile.html', student_data=student_data, classes=classes)


@student.route('/change_student_form', methods=['GET', 'POST'])
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
      return redirect(url_for('student.students_profile'))
  return render_template('change_student_form.html', form=form, student=student)
