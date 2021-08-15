from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length


class ChangeTeacherForm(FlaskForm):
	first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=20)])
	last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=20)])
	university = StringField('University', validators=[DataRequired()])
	major = SelectField("Major", choices=['Biology', 'Chemistry', 'History'], validators=[DataRequired()])
	submit = SubmitField('Update')
