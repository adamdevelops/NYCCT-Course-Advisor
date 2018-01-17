from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Programs, Base, Courses, Departments
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


engine = create_engine('sqlite:///coursecatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# App Routes
# Dashboard where a list of recent movies added to the database is shown.
@app.route('/')
@app.route('/dashboard/')
def creditDashboard():
    courses = session.query(Courses).limit(10).all()
    depts = session.query(Departments).all()
    return render_template('dashboard.html', courses = courses, depts = depts)

@app.route('/depts')
def deptDashboard():
    courses = session.query(Courses).limit(10).all()
    depts = session.query(Departments).all()
    return render_template('departments_dashboard.html', courses = courses, depts = depts)

@app.route('/programs')
def progDashboard():
    programs = session.query(Programs).limit(10).all()
    depts = session.query(Departments).all()
    return render_template('programs_dashboard.html', progs = programs, depts = depts)

@app.route('/courses')
def courseDashboard():
    courses = session.query(Courses).limit(10).all()
    return render_template('course_dashboard.html', courses = courses)

@app.route('/prereq')
def courseDashboard():
    courses = session.query(Prereq).limit(10).all()
    return render_template('course_dashboard.html', courses = courses)

@app.route('/coreq')
def courseDashboard():
    courses = session.query(Coreq).limit(10).all()
    return render_template('course_dashboard.html', courses = courses)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
