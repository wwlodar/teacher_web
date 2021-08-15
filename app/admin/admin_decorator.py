from flask_login import current_user, login_required
from flask import url_for, flash, redirect
from functools import wraps
from app.models import Admin


def is_admin():
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if current_user.is_authenticated and current_user == Admin.query.filter_by(email=current_user.email).first():
				return func(*args, **kwargs)
			else:
				flash("You are not an administrator", "warning")
				return redirect(url_for("main.homepage"))
		return login_required(wrapper)
	return decorator
