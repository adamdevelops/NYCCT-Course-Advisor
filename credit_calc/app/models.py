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
    progs = db.relationship('Programs', backref='dept')
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
    # prereq = db.relationship('Prereq', backref='programs', lazy='dynamic')
    # coreq = db.relationship('Coreq', backref='programs', lazy='dynamic')


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

# Database Table for Prereq courses
prereq = db.Table('prereq',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id')),
    db.Column('prereq_id', db.Integer, db.ForeignKey('courses.id'))
)

# Database Table for Coreq courses
coreq = db.Table('coreq',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id')),
    db.Column('coreq_id', db.Integer, db.ForeignKey('courses.id'))
)

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(8), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    progs_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    prereqs = db.relationship(
        'Courses', secondary=prereq,
        primaryjoin=(prereq.c.course_id == id),
        secondaryjoin=(prereq.c.prereq_id == id),
        backref=db.backref('prereq', lazy='dynamic'), lazy='dynamic')
    coreqs = db.relationship(
        'Courses', secondary=coreq,
        primaryjoin=(coreq.c.course_id == id),
        secondaryjoin=(coreq.c.coreq_id == id),
        backref=db.backref('coreq', lazy='dynamic'), lazy='dynamic')
    children = db.relationship("Courses",
                backref=db.backref('parent', remote_side=[id])
            )


    # Add Prereq course to a Course
    def add_prereq(self, course):
        if not self.is_preq(course):
            self.prereqs.append(course)

    # For course ID see if the selected course is already a prereq
    def is_preq(self, course):
        return self.prereqs.filter(
            prereq.c.prereq_id == course.id).count() > 0

     # def all_prereqs(self, course):
     #     return self.prereqs.filter(
     #         prereq.c.course_id == course.id).query().all()

    # Add Coreq course to a Course
    def add_coreq(self, course):
        if not self.is_coreq(course):
            self.coreqs.append(course)

    # For course ID see if the selected course is already a coreq
    def is_coreq(self, course):
        return self.coreqs.filter(
            coreq.c.coreq_id == course.id).count() > 0

    # def __init__(self, name, parent=None):
    #     self.name = name
    #     self.parent = parent

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'dept_id': self.dept_id
        }

# query_prereqs = Courses.query.join(prereq).
#     filter(prereq.c.courses_id == Courses.id and prereq.c.prereq_id == Courses.id).all()

# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(80), nullable=False)


# Database Relationships
# One to Many
# Depts -> Course, Program -> Many Courses
# Many to Many
# Courses -> Prereq, Courses -> Coreq
