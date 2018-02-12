from flask import render_template, flash, redirect, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import Departments, Programs


# App Routes
# Dashboard where a list of recent movies added to the database is shown.
@app.route('/')
@app.route('/dashboard/')
def creditDashboard():
    depts = Departments.query.all()
    return render_template('dashboard.html', depts = depts)

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
def prereqDashboard():
    courses = session.query(Prereq).limit(10).all()
    return render_template('course_dashboard.html', courses = courses)

@app.route('/coreq')
def coreqDashboard():
    courses = session.query(Coreq).limit(10).all()
    return render_template('course_dashboard.html', courses = courses)
