from flask import Flask
from app.Config import Config
from .extensions import (
  bcrypt,
  db,
  login_manager,
  csrf
)


def register_extensions(app):
  db.init_app(app)
  csrf.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)


def create_app(config_class=Config):
  app = Flask(__name__, template_folder='templates')
  app.config.from_object(Config)

  from app.student.routes import student
  from app.main.routes import main
  from app.teacher.routes import teacher
  from app.admin.routes import admin
  app.register_blueprint(student)
  app.register_blueprint(teacher)
  app.register_blueprint(main)
  app.register_blueprint(admin)
  register_extensions(app)
  with app.app_context():
    db.create_all()
    print(db.engine.table_names())
  return app


from app.admin import routes
from app.main import routes
from app.student import routes
from app.teacher import routes
