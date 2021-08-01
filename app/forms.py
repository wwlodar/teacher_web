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
    password = PasswordField('Password', validators=[DataRequired()])
    university = StringField('University', validators=[DataRequired()])
    subjects = SelectField('Subjects', choices=["Biology", "Chemistry", "History"])
    submit = SubmitField('Submit')


class RegisterFormStudent(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    date_of_birth = DateField('Date of birth', format='%Y-%m-%d')
    parents_name = StringField("Parent's name", validators=[DataRequired(), Length(min=2, max=20)])
    parents_phone = IntegerField("Parent's phone", validators=[DataRequired(), NumberRange(min=100000000, max=999999999,
        message=('Proszę wprowadź poprawny numer'))])
    submit = SubmitField('Submit')

