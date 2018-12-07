from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from app import login

coursedept = db.Table('coursedept',
    db.Column('dept_id', db.Integer, db.ForeignKey('departments.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
)

class Departments(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    progs = db.relationship('Programs', backref='departments', lazy='dynamic')
    course_depts = db.relationship('Courses', backref='dept')
    # db.relationship('Courses', secondary=coursedept,  backref='course_department', lazy='dynamic')
#    prereq = db.relationship('Prereq', backref='departments', lazy='dynamic')
#    coreq = db.relationship('Coreq', backref='departments', lazy='dynamic')


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'code': self.code,
            'course_depts':self.course_depts
        }


class Programs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    courses = db.relationship('Courses', backref='programs', lazy='dynamic')
    prereq = db.relationship('Prereq', backref='programs', lazy='dynamic')
    coreq = db.relationship('Coreq', backref='programs', lazy='dynamic')


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(8), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    progs_id = db.Column(db.Integer, db.ForeignKey('programs.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'dept_id': self.dept_id
        }


class Prereq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(8), nullable=False)
    prereq_code = db.Column(db.String(8), nullable=False)
    prog_id = db.Column(db.String(80), db.ForeignKey('programs.id'))


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'prog_id': self.prog_id
        }


class Coreq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(8), nullable=False)
    coreq_code = db.Column(db.String(8), nullable=False)
    prog_id = db.Column(db.String(80), db.ForeignKey('programs.id'))


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'prog_id': self.prog_id
        }

# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(80), nullable=False)


# Database Relationships
# One to Many
# Depts -> Course, Program -> Many Courses
# Many to Many
# Courses -> Prereq, Courses -> Coreq
