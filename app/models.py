from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from app import login


class Departments(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    progs = db.relationship('Programs', backref='dept')
    course_depts = db.relationship('Courses', backref='dept')
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
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

# Programs / Majors
class Programs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    major_short = db.Column(db.String(8), nullable=False)
    degree_id = db.Column(db.Integer, db.ForeignKey('degree.id'))
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    WI_inmajor = db.Column(db.Boolean)
    WI_ingened = db.Column(db.Boolean)
    # prereq = db.relationship('Prereq', backref='programs', lazy='dynamic')
    # coreq = db.relationship('Coreq', backref='programs', lazy='dynamic')


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class Degree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    type_short = db.Column(db.String(4), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    years = db.Column(db.Integer, nullable=False)
    programs = db.relationship('Programs', backref='degree')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'type': self.type,
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

    def __repr__(self):
        return '<Course: {} {}>'.format(self.code, self.id)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'dept_id': self.dept_id
        }

class Schools(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    school_acronym = db.Column(db.String(4), nullable=False)
    depts = db.relationship('Departments', backref='school')


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'school_acronym': self.school_acronym
        }

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Creates a many-to-one relation (many users to one role but one user can have only one role)
    # the relationship is called *role* and is defined in the Role model
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    advisor_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Advisor ID

    # Defines both advisees and advisor relationships
    # Advisees would be an InstrumentedList of User items and advisor will be an User
    advisees = db.relationship('User', backref=db.backref('advisor', remote_side=[id]))

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def userExists(cls, user):
        u = User.query.filter_by(username=user).first()
        return u

    @classmethod
    def loginUser(cls, username, password):
        u = cls.userExists(username)
        if u and u.check_password(password):
            return u

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(140))

    # Many users can have a given role
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.role_name)


# Database Relationships
# One to Many
# Depts -> Course, Program -> Many Courses
# Many to Many
# Courses -> Prereq, Courses -> Coreq
