from flask import render_template, flash, redirect, request, url_for
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import Departments, Programs, Courses


# App Routes
# Dashboard where a list of recent movies added to the database is shown.
@app.route('/')
@app.route('/dashboard/')
def creditDashboard():
    depts = Departments.query.all()
    progs = Courses.query.all()
    pros = Programs.query.all()
    return render_template('dashboard.html', depts = depts, courses = progs, pros = pros)

# Departments Dashboard
@app.route('/depts')
def deptDashboard():
    courses = Courses.query.all()
    depts = Departments.query.all()
    pros = Programs.query.all()
    return render_template('departments_dashboard.html', courses = courses, depts = depts)

# CRUD routes for Departments
@app.route('/depts/create', methods=['GET', 'POST'])
def createDeptForm():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        newDept = Departments(name = name, code= code)
        db.session.add(newDept)
        flash('%s was Successfully Created' % newDept.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        return render_template('createdept_form.html')

@app.route('/depts/edit/<int:dept_id>', methods=['GET', 'POST'])
def editDeptForm(dept_id):
    if request.method == 'POST':
        editedDept = Departments.query.filter_by(id=dept_id).one()
        editedDept.name = request.form['name']
        editedDept.code = request.form['code']
        db.session.add(editedDept)
        flash('%s was Successfully Edited' % editedDept.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        editedDept = Departments.query.filter_by(id=dept_id).one()
        return render_template('editdept_form.html', dept = editedDept)

@app.route('/depts/delete/<int:dept_id>', methods=['GET', 'POST'])
def deleteDeptForm(dept_id):
    if request.method == 'POST':
        deletedDept = Departments.query.filter_by(id=dept_id).one()
        db.session.delete(deletedDept)
        flash('%s was Successfully Deleted' % deletedDept.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        deletedDept = Departments.query.filter_by(id=dept_id).one()
        return render_template('deletedept_form.html', dept = deletedDept)

@app.route('/programs')
def progDashboard():
    programs = Programs.query.all()
    depts = Departments.query.all()
    return render_template('programs_dashboard.html', progs = programs, depts = depts)

@app.route('/courses')
def courseDashboard():
    courses = Courses.query.all()
    return render_template('course_dashboard.html', courses = courses)

@app.route('/prereq')
def prereqDashboard():
    courses = session.query(Prereq).limit(10).all()
    return render_template('course_dashboard.html', courses = courses)

@app.route('/coreq')
def coreqDashboard():
    courses = session.query(Coreq).limit(10).all()
    return render_template('course_dashboard.html', courses = courses)





@app.route('/login')
def loginForm():
    return render_template('login.html')
