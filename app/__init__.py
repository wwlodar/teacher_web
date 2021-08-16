from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from app.Config import Config

db = SQLAlchemy()
csrf = CSRFProtect()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'login_user'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
  app = Flask(__name__, template_folder='templates')
  app.config.from_object(Config)

  db.init_app(app)
  csrf.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)

  from app.student.routes import student
  from app.main.routes import main
  from app.teacher.routes import teacher
  from app.admin.routes import admin
  app.register_blueprint(student)
  app.register_blueprint(teacher)
  app.register_blueprint(main)
  app.register_blueprint(admin)

  return app


from app.admin import routes
from app.main import routes
from app.student import routes
from app.teacher import routes
