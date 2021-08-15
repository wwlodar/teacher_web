from flask import render_template, url_for, flash, redirect, Blueprint
from app.models import db, Teacher, Classes, User
from app.teacher.forms import ChangeTeacherForm
from app import bcrypt, app
from flask_login import current_user, logout_user, login_required
import flask_login

teacher = Blueprint('teacher', __name__)


@teacher.route('/teacher_profile')
@login_required
def teachers_profile():
  teacher_data = Teacher.query.filter_by(email=current_user.email).first()
  classes = [(t.subject + " " + t.weekday + " " + t.hour) for t in Classes.query.filter_by
  (teacher_id=current_user.id).all()]
  return render_template('teacher_profile.html', teacher_data=teacher_data, classes=classes)


@teacher.route('/change_teacher_form', methods=['GET', 'POST'])
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
      return redirect(url_for('teacher.teachers_profile'))
  return render_template('change_teacher_form.html', form=form, teacher=teacher)

