from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
csrf = CSRFProtect()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'login_user'
login_manager.login_message_category = 'info'
