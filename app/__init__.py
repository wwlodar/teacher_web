from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


app = Flask(__name__, template_folder='templates')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba544'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()
csrf.init_app(app)


db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


association_table = db.Table('association', User.metadata,
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')))


class Student(User):
    __tablename__ = "students"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    teachers = db.relationship("Teacher", secondary=association_table)
    def __repr__(self):
        return f"('{self.username}', '{self.email}', '{self.password}')"


class Teacher(User):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    students = db.relationship("Student", secondary=association_table)
    def __repr__(self):
        return f"('{self.username}', '{self.email}', '{self.password}')"


class Admin (User):
    __tablename__ = "Admins"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


db.create_all()
print(db.engine.table_names())

from app import main
