from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

login = LoginManager()
db = SQLAlchemy()


class CourseModel(db.Model):
    __tablename__ = "course_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(), unique=True)
    course_duration = db.Column(db.Integer())
    course_description = db.Column(db.String())
    technology = db.Column(db.String())
    launch_url = db.Column(db.String())

    def __init__(self, course_name, course_duration, course_description, technology, launch_url):
        self.course_name = course_name
        self.course_duration = course_duration
        self.course_description = course_description
        self.technology = technology
        self.launch_url = launch_url

    def __repr__(self):
        return f"{self.course_name}"


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))