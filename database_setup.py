import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, desc
from sqlalchemy import types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    code = Column(String(80), nullable=False)
    name = Column(String(80), nullable=False)
    #created = Column(DateTime)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'code': self.code
        }


class Programs(Base):
    __tablename__ = 'programs'

    id = Column(Integer, primary_key=True)
    code = Column(String(80), nullable=False)
    name = Column(String(80), nullable=False)
    level = Column(String(80), nullable=False)
    # dept_id = Column(String(80), ForeignKey('dept.id'))
    # dept = relationship(Departments)
    #created = Column(DateTime)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Courses(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    dept_code = Column(String(80), ForeignKey('dept.code'))
    dept = relationship("departments")
    #created = Column(DateTime)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'prog_id': self.prog_id
        }


class Prereq(Base):
    __tablename__ = 'prereq'

    id = Column(Integer, primary_key=True)
    course_code = Column(String(80), nullable=False)
    prereq_code = Column(String(80), nullable=False)
    #prog_id = Column(String(80), ForeignKey('programs.id'))
    #created = Column(DateTime)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'prog_id': self.prog_id
        }

class Coreq(Base):
    __tablename__ = 'coreq'

    id = Column(Integer, primary_key=True)
    course_code = Column(String(80), nullable=False)
    coreq_code = Column(String(80), nullable=False)
    #prog_id = Column(String(80), ForeignKey('programs.id'))
    #created = Column(DateTime)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'prog_id': self.prog_id
        }


engine = create_engine('sqlite:///coursecatalog.db')


Base.metadata.create_all(engine)
