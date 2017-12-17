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

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    prog_id = Column(String(80), ForeignKey('programs.id'))
    programs = relationship(Programs)
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
    prog_id = Column(String(80), ForeignKey('programs.id'))
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
