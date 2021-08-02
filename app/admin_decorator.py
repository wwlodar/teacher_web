from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request, Blueprint
from functools import wraps


def is_admin():
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if current_user.is_authenticated and current_user.email == "m@m.m":
				return func(*args, **kwargs)
			else:
				flash("You are not an administrator", "warning")
				return redirect(url_for("homepage"))

		return login_required(wrapper)

	return decorator
