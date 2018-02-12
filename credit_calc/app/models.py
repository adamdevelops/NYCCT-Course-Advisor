from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from app import login


class Departments(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    progs = db.relationship('Programs', backref='departments', lazy='dynamic')
    #courses = db.relationship('Courses', backref='departments', lazy='dynamic')
    #created = db.Column(DateTime)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'code': self.code
        }


class Programs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(80), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    #courses = db.relationship('Courses', backref='courses', lazy='dynamic')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


# class Courses(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     dept_id = db.Column(db.Integer, db.ForeignKey('dept.id'))
    #created = db.Column(DateTime)
    #
    #
    # @property
    # def serialize(self):
    #     """Return object data in easily serializeable format"""
    #     return {
    #         'name': self.name,
    #         'id': self.id,
    #         'prog_id': self.prog_id
    #     }


# class Prereq(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     course_code = db.Column(db.String(80), nullable=False)
#     prereq_code = db.Column(db.String(80), nullable=False)
    #prog_id = db.Column(db.String(80), ForeignKey('programs.id'))
    #created = db.Column(DateTime)
    #
    #
    # @property
    # def serialize(self):
    #     """Return object data in easily serializeable format"""
    #     return {
    #         'name': self.name,
    #         'id': self.id,
    #         'prog_id': self.prog_id
    #     }

# class Coreq(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     course_code = db.Column(db.String(80), nullable=False)
#     coreq_code = db.Column(db.String(80), nullable=False)
#
#
#     @property
#     def serialize(self):
#         """Return object data in easily serializeable format"""
#         return {
#             'name': self.name,
#             'id': self.id,
#             'prog_id': self.prog_id
#         }
