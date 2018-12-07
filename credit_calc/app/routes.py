from flask import render_template, flash, redirect, request, url_for
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import Departments, Programs, Courses, coursedept


# App Routes
# Dashboard where a list of recent movies added to the database is shown.
@app.route('/')
@app.route('/dashboard/')
def creditDashboard():
    depts = Departments.query.all()
    progs = Courses.query.all()
    pros = Programs.query.all()
    return render_template('dashboard.html', depts = depts, courses = progs, pros = pros)

@app.route('/login', methods=['GET', 'POST'])
def userLogin():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        # if username is not in database test case
            #
        return redirect(url_for('creditDashboard'))
    else:
        return render_template('createdept_form.html')

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

# Specific Department Page
@app.route('/depts/<int:dept_id>')
def deptDetail(dept_id):
    Department = Departments.query.filter_by(id=dept_id).one()
    return render_template('departments_detail.html', dept = Department)

# Programs Dashboard
@app.route('/programs')
def progDashboard():
    programs = Programs.query.all()
    depts = Departments.query.all()
    return render_template('programs_dashboard.html', progs = programs, depts = depts)

# CRUD routes for Programs
@app.route('/programs/create', methods=['GET', 'POST'])
def createProgramForm():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        degree = request.form['degree']
        newProgram = Programs(name = name, code= code, degree = degree)
        db.session.add(newProgram)
        flash('%s was Successfully Created' % newProgram.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        return render_template('createprogram_form.html')

@app.route('/programs/edit/<int:program_id>', methods=['GET', 'POST'])
def editProgramForm(program_id):
    if request.method == 'POST':
        editedProgram = Programs.query.filter_by(id=program_id).one()
        editedProgram.name = request.form['name']
        editedProgram.code = request.form['code']
        editedProgram.degree = request.form['degree']
        db.session.add(editedProgram)
        flash('%s was Successfully Edited' % editedProgram.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        editedProgram = Programs.query.filter_by(id=program_id).one()
        return render_template('editprogram_form.html', program = editedProgram)

@app.route('/programs/delete/<int:program_id>', methods=['GET', 'POST'])
def deleteProgramForm(program_id):
    if request.method == 'POST':
        deletedProgram = Programs.query.filter_by(id=program_id).one()
        db.session.delete(deletedProgram)
        flash('%s was Successfully Deleted' % deletedProgram.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        deletedProgram = Programs.query.filter_by(id=program_id).one()
        return render_template('deleteprogram_form.html', program = deletedProgram)

# Specific Programs Page
@app.route('/programs/<int:prog_id>')
def programDetail(prog_id):
    Program = Programs.query.filter_by(id=prog_id).one()
    return render_template('program_detail.html', program = Program)

# Course Dashboard
@app.route('/courses')
def courseDashboard():
    courses = Courses.query.all()
    return render_template('course_dashboard.html', courses = courses)

# CRUD routes for Courses
@app.route('/courses/create', methods=['GET', 'POST'])
def createCourseForm():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        credits = request.form['credits']
        newCourse = Courses(name = name, code= code, credits = int(credits))
        db.session.add(newCourse)
        flash('%s was Successfully Created' % newCourse.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        return render_template('createCourse_form.html')

@app.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
def editCourseForm(course_id):
    if request.method == 'POST':
        editedCourse = Courses.query.filter_by(id=course_id).one()
        editedCourse.name = request.form['name']
        editedCourse.code = request.form['code']
        editedCourse.credits = int(request.form['credits'])
        db.session.add(editedCourse)
        flash('%s was Successfully Edited' % editedCourse.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        editedCourse = Courses.query.filter_by(id=course_id).one()
        return render_template('editCourse_form.html', course = editedCourse)

@app.route('/courses/delete/<int:course_id>', methods=['GET', 'POST'])
def deleteCourseForm(course_id):
    if request.method == 'POST':
        deletedCourse = Courses.query.filter_by(id=course_id).one()
        db.session.delete(deletedCourse)
        flash('%s was Successfully Deleted' % deletedCourse.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        deletedCourse = Courses.query.filter_by(id=course_id).one()
        return render_template('deleteCourse_form.html', course = deletedCourse)

# Specific Courses Page
@app.route('/courses/<int:course_id>')
def courseDetail(course_id):
    Course = Courses.query.filter_by(id=course_id).one()
    CourseDepts = Courses.query.join(coursedept, (coursedept.c.course_id == Course.id)).filter(coursedept.c.user_id == Course.course_department)
    return render_template('course_detail.html', course = Course, coursedepts = CourseDepts)

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
