from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired, Length,  NumberRange


class ChangeStudentForm(FlaskForm):
	first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
	last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
	date_of_birth = DateField('Date of birth', format='%Y-%m-%d')
	parents_name = StringField("Parent's name", validators=[DataRequired(), Length(min=2, max=20)])
	parents_phone = IntegerField("Parent's phone", validators=[DataRequired(), NumberRange(min=100000000, max=999999999,)])
	submit = SubmitField('Submit')