from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


class User(db.Model, UserMixin):
  __tablename__ = "user"
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)


association_teacher_student_table = db.Table('association_teacher_student',
                                             User.metadata,
                                             db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                                             db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')))

association_class_student_table = db.Table('association_class_student',
                                           db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                                           db.Column('class_id', db.Integer, db.ForeignKey('classes.id')))


class Student(User):
  __tablename__ = "students"
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  teachers = db.relationship("Teacher", secondary=association_teacher_student_table, backref=db.backref('students',
                                                                                                        lazy='dynamic'))
  classes = db.relationship("Classes", secondary=association_class_student_table, back_populates='students',
                            lazy='dynamic')
  date_of_birth = db.Column(db.String)
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)
  parents_name = db.Column(db.String)
  parents_phone = db.Column(db.String)

  def __repr__(self):
    return f"('{self.email}', '{self.password}', '{self.first_name}')"


class Teacher(User):
  __tablename__ = "teachers"
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)
  university = db.Column(db.String)
  subjects = db.Column(db.String)
  major = db.Column(db.String)

  def __repr__(self):
    return f"('{self.email}', '{self.last_name}', '{self.first_name}')"


class Classes(db.Model):
  __tablename__ = "classes"
  id = db.Column(db.Integer, primary_key=True)
  weekday = db.Column(db.String)
  subject = db.Column(db.String)
  teacher_id = db.Column(db.ForeignKey('teachers.id'))
  hour = db.Column(db.String)
  students = db.relationship("Student", secondary=association_class_student_table, back_populates='classes',
                             lazy='dynamic')

  def __repr__(self):
    return f"('{self.teacher_id}', '{self.weekday}', '{self.subject}')"

  def descri(self):
    return f"('{self.weekday}')"


class Admin(User):
  __tablename__ = "Admins"
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


db.create_all()
print(db.engine.table_names())
