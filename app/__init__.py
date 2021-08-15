from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

app = Flask(__name__, template_folder='templates')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba544'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
login_manager = LoginManager(app)
login_manager.login_view = 'login_user'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()
csrf.init_app(app)

db = SQLAlchemy(app)

from app.student.routes import student
from app.main.routes import main
from app.teacher.routes import teacher
from app.admin.routes import admin
app.register_blueprint(student)
app.register_blueprint(teacher)
app.register_blueprint(main)
app.register_blueprint(admin)

from app.admin import routes
