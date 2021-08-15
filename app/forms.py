from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app import db, login_manager
from app import User


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class RegisterFormTeacher(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
	last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	university = StringField('University', validators=[DataRequired()])
	major = SelectField("Major", choices=['Biology', 'Chemistry', 'History'], validators=[DataRequired()])
	submit = SubmitField('Submit')


class RegisterFormStudent(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	date_of_birth = DateField('Date of birth', format='%Y-%m-%d')
	first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
	last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
	parents_name = StringField("Parent's name", validators=[DataRequired(), Length(min=2, max=20)])
	parents_phone = IntegerField("Parent's phone", validators=[DataRequired(), NumberRange(min=100000000, max=999999999,)])
	submit = SubmitField('Submit')


class AddNewClass(FlaskForm):
	teacher_id = SelectField(coerce=int, validators=[DataRequired()])
	subject = SelectField("Subjects", choices=['Biology', 'Chemistry', 'History'], validators=[DataRequired()])
	weekday = SelectField("Day of the class", choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], validators=[DataRequired()])
	hour = SelectField("Time of class", choices=["4-5 p.m.", "5-6 p.m.", "6-7 p.m."])
	submit = SubmitField('Submit')


class AssignStudent(FlaskForm):
	student_id = SelectField(validators=[DataRequired()])
	classes_id = SelectField(validators=[DataRequired()])
	submit = SubmitField('Submit')


class UpdateClass(FlaskForm):
	teacher_id = SelectField(coerce=int, validators=[DataRequired()])
	subject = SelectField("Subjects", choices=['Biology', 'Chemistry', 'History'], validators=[DataRequired()])
	weekday = SelectField("Day of the class", choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], validators=[DataRequired()])
	hour = SelectField("Time of class", choices=["4-5 p.m.", "5-6 p.m.", "6-7 p.m."])
	submit = SubmitField('Update')


class ChooseClass(FlaskForm):
	classes_id = SelectField(validators=[DataRequired()])
	submit = SubmitField('Update')


class ChangeTeacherForm(FlaskForm):
	first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
	last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
	university = StringField('University', validators=[DataRequired()])
	major = SelectField("Major", choices=['Biology', 'Chemistry', 'History'], validators=[DataRequired()])
	submit = SubmitField('Update')


class ChangeStudentForm(FlaskForm):
	first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
	last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
	date_of_birth = DateField('Date of birth', format='%Y-%m-%d')
	parents_name = StringField("Parent's name", validators=[DataRequired(), Length(min=2, max=20)])
	parents_phone = IntegerField("Parent's phone", validators=[DataRequired(), NumberRange(min=100000000, max=999999999,)])
	submit = SubmitField('Submit')