from flask import render_template, flash, redirect, request, url_for
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from flask_user import roles_required, UserManager
from werkzeug.urls import url_parse
from app.models import Departments, Programs, Courses, Degree, Schools, User, Role
from app.forms import LoginForm, SignupForm


# App Routes
# Dashboard where a list of recent movies added to the database is shown.
@app.route('/')
@app.route('/dashboard/')
def creditDashboard():
    depts = Departments.query.all()
    courses = Courses.query.all()
    majors = Programs.query.all()
    return render_template('dashboard.html', depts = depts, courses = courses, pros = majors)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # User is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('creditDashboard'))
    form = LoginForm()
    # form.['language'].choices = [(d.id, d.name) for d in depts]
    if form.validate_on_submit():
        user = User.userExists(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        print (form.remember_me.data)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('creditDashboard')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('creditDashboard'))

# @app.route('/login', methods=['GET', 'POST'])
# def userLogin():
#     if request.method == 'POST':
#         user = request.form['user']
#         password = request.form['password']
#
#         if User.loginUser(user, password):
#             flash('%s was Successfully logged in' % user)
#             return redirect(url_for('creditDashboard'))
#         else:
#             return render_template('login.html')
#     else:
#         return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def userSignup():
    # User is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('creditDashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        newUser = User(username = form.username.data, email = form.email.data)
        newUser.set_password(form.password.data)
        db.session.add(newUser)
        db.session.commit()
        flash('%s was Successfully Created' % newUser.username)
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

# @app.route('/signup', methods=['GET', 'POST'])
# def userSignup():
#     if request.method == 'POST':
#         user = request.form['user']
#         password = request.form['password']
#         email = request.form['email']
#
#         # if username is not in database test case
        # newUser = User(username = user, email = email)
        # if not User.userExists(newUser.username):
        #     newUser.set_password(password)
        #     db.session.add(newUser)
        #     db.session.commit()
        #     flash('%s was Successfully Added' % newUser.username)
        #     return redirect(url_for('creditDashboard'))
#         else:
#             return render_template('signup.html')
#     else:
#         return render_template('signup.html')

# Departments Dashboard
@app.route('/depts')
def deptDashboard():
    courses = Courses.query.all()
    depts = Departments.query.all()
    pros = Programs.query.all()
    return render_template('departments_dashboard.html', courses = courses, depts = depts)

# CRUD routes for Departments
@app.route('/depts/create', methods=['GET', 'POST'])
# @roles_required('Advisor')
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
        if current_user.role_id == 2:   # Only allow access to page if logged in user is a Advisor.
            return render_template('createdept_form.html')
        else:
            flash('You do not have correct privilege level to access page.')
            return redirect(url_for('creditDashboard'))

@app.route('/depts/edit/<int:dept_id>', methods=['GET', 'POST'])
@login_required
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
        if current_user.role_id == 2:   # Only allow access to page if logged in user is a Advisor.
            editedDept = Departments.query.filter_by(id=dept_id).one()
            return render_template('editdept_form.html', dept = editedDept)
        else:
            flash('You do not have correct privilege level to access page.')
            return redirect(url_for('creditDashboard'))

@app.route('/depts/delete/<int:dept_id>', methods=['GET', 'POST'])
@login_required
def deleteDeptForm(dept_id):
    if request.method == 'POST':
        deletedDept = Departments.query.filter_by(id=dept_id).one()
        db.session.delete(deletedDept)
        flash('%s was Successfully Deleted' % deletedDept.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        if current_user.role_id == 2:   # Only allow access to page if logged in user is a Advisor.
            deletedDept = Departments.query.filter_by(id=dept_id).one()
            return render_template('deletedept_form.html', dept = deletedDept)
        else:
            flash('You do not have correct privilege level to access page.')
            return redirect(url_for('creditDashboard'))

# Specific Department Page
@app.route('/depts/<int:dept_id>')
def deptDetail(dept_id):
    department = Departments.query.filter_by(id=dept_id).one()
    print(department.progs)
    # print(department.progs.id)
    return render_template('departments_detail.html', dept = department)

# Programs Dashboard
@app.route('/programs')
def progDashboard():
    programs = Programs.query.all()
    depts = Departments.query.all()
    return render_template('programs_dashboard.html', progs = programs, depts = depts)

# CRUD routes for Programs
@app.route('/programs/create', methods=['GET', 'POST'])
@login_required
def createProgramForm():
    if request.method == 'POST':
        name = request.form['name']
        major_short = request.form['major_short']
        degree_id = request.form['degree']
        degree = Degree.query.filter_by(id=degree_id).one()
        newProgram = Programs(name = name, major_short= major_short, degree = degree)
        db.session.add(newProgram)
        flash('%s was Successfully Created' % newProgram.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        if current_user.role_id == 2:   # Only allow access to page if logged in user is a Advisor.
            degrees = Degree.query.all()
            return render_template('createprogram_form.html', degrees=degrees)
        else:
            flash('You do not have correct privilege level to access page.')
            return redirect(url_for('creditDashboard'))

@app.route('/programs/edit/<int:program_id>', methods=['GET', 'POST'])
@login_required
def editProgramForm(program_id):
    if request.method == 'POST':
        editedProgram = Programs.query.filter_by(id=program_id).one()
        editedProgram.name = request.form['name']
        editedProgram.code = request.form['code']
        degree_id = request.form['degree']
        degree = Degree.query.filter_by(id=degree_id).one()
        editedProgram.degree = degree
        print('editprogram object')
        print(editedProgram)
        db.session.add(editedProgram)
        flash('%s was Successfully Edited' % editedProgram.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        if current_user.role_id == 2:   # Only allow access to page if logged in user is a Advisor.
            editedProgram = Programs.query.filter_by(id=program_id).one()
            degrees = Degree.query.all()
            return render_template('editprogram_form.html', program = editedProgram, degrees=degrees)
        else:
            flash('You do not have correct privilege level to access page.')
            return redirect(url_for('creditDashboard'))

@app.route('/programs/delete/<int:program_id>', methods=['GET', 'POST'])
@login_required
def deleteProgramForm(program_id):
    if request.method == 'POST':
        deletedProgram = Programs.query.filter_by(id=program_id).one()
        db.session.delete(deletedProgram)
        flash('%s was Successfully Deleted' % deletedProgram.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        if current_user.role_id == 2:   # Only allow access to page if logged in user is a Advisor.
            deletedProgram = Programs.query.filter_by(id=program_id).one()
            return render_template('deleteprogram_form.html', program = deletedProgram)
        else:
            flash('You do not have correct privilege level to access page.')
            return redirect(url_for('creditDashboard'))

# Specific Programs Page
@app.route('/programs/<int:prog_id>')
def programDetail(prog_id):
    Program = Programs.query.filter_by(id=prog_id).one()
    return render_template('program_detail.html', program = Program)

# Course Dashboard
@app.route('/courses')
def courseDashboard():
    courses = Courses.query.order_by(Courses.dept_id).all()
    return render_template('course_dashboard.html', courses = courses)

# CRUD routes for Courses
@app.route('/courses/create', methods=['GET', 'POST'])
@login_required
def createCourseForm():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        credits = request.form['credits']
        dept_id = request.form['department']
        # multiselect = request.form.getlist('mymultiselect')
        # preq_course_id = request.form['preq_course']
        # coreq_course_id = request.form['coreq_course']
        dept = Departments.query.filter_by(id=dept_id).one()
        # preq_course = Courses.query.filter_by(id=preq_course_id).one()
        # coreq_course = Courses.query.filter_by(id=coreq_course_id).one()
        # Create new Course object to database
        newCourse = Courses(name = name, code= code, credits = int(credits), dept = dept)
        # Add Prereq and Coreq courses to new Course object
        # newCourse.add_prereq(preq_course)
        # newCourse.add_coreq(coreq_course)
        # Add Course object to database
        db.session.add(newCourse)
        flash('%s was Successfully Created' % newCourse.name)
        print(">>>>>>Before commit <<<<<<<")
        db.session.commit()
        return redirect(url_for('creditDashboard'))
        # print("***************************After commit")
        # print(newCourse)
        # course = Courses.query.filter_by(id = newCourse.id).one()
        # return redirect(url_for('createCoursePreReqForm', course_id=newCourse.id))
    else:
        if current_user.role_id == 2:   # Only allow access to page if logged in user is a Advisor.
            depts = Departments.query.all()
            courses = Courses.query.all()
            return render_template('createcourse_form.html', depts = depts, courses = courses)
        else:
            flash('You do not have correct privilege level to access page.')
            return redirect(url_for('creditDashboard'))

@app.route('/courses/create/<int:course_id>', methods=['GET', 'POST'])
def createCoursePreReqForm(course_id):
    if request.method == 'POST':
        # Query for new Course object we created so we can later use instance method for adding prereqs
        newCourse = Courses.query.filter_by(name=course_name).one()

        # Grab pre-req course selection from form and add it as pre-req to newCourse object
        preq_course_id = request.form['preq_course']
        preq_course = Courses.query.filter_by(id=preq_course_id).one()
        newCourse.add_prereq(preq_course)

        flash('%s was Successfully Added as prerequiste' % preq.name)
        return redirect(url_for('creditDashboard'))
    else:
        newCourse = Courses.query.filter_by(id = course_id).one()
        print(newCourse)
        return render_template('createCoursePreReq_form.html', course= newCourse)

@app.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def editCourseForm(course_id):
    if request.method == 'POST':
        editedCourse = Courses.query.filter_by(id=course_id).one()
        editedCourse.name = request.form['name']
        editedCourse.code = request.form['code']
        editedCourse.credits = int(request.form['credits'])

        prereqs = request.form.getlist('prereq')
        print('Result of prereqs:')
        print(prereqs)
        print(prereqs[0])
        print(prereqs[0].split(','))
        print('Result of prereqs indexes:')

        if not(prereqs[0] == ''):
            for prereq_course_id in prereqs[0].split(','):
                print(id)
                print('....')
                prereq_course = Courses.query.filter_by(id=prereq_course_id).one()
                print(prereq_course)
                editedCourse.add_coreq(prereq_course)
        else:
            print('No prereqs')


        # print('get multivalue')
        coreqs = request.form.getlist('coreq')
        print('Result of coreqs:')
        print(coreqs)
        print(coreqs[0])
        # print(coreqs[0].split(','))
        if not(coreqs == ''):
            print('empty')
        if not(coreqs[0] == ''):
            print('emptier')
        print('Result of coreqs indexes:')

        if not(coreqs[0] == ''):
            for coreq_course_id in coreqs[0].split(','):
                print(coreq_course_id)
                print('....')
                if coreq_course_id == '':
                    print('not empty')
                coreq_course = Courses.query.filter_by(id=coreq_course_id).one()
                print(coreq_course)
                editedCourse.add_coreq(coreq_course)
        else:
            print('No coreqs')

        db.session.add(editedCourse)
        flash('%s was Successfully Edited' % editedCourse.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        if current_user.role_id == 2:   # Only allow access to page if logged in user is a Advisor.
            editedCourse = Courses.query.filter_by(id=course_id).one()
            depts = Departments.query.all()
            return render_template('editCourse_form.html', course = editedCourse, depts = depts)
        else:
            flash('You do not have correct privilege level to access page.')
            return redirect(url_for('creditDashboard'))

@app.route('/courses/delete/<int:course_id>', methods=['GET', 'POST'])
@login_required
def deleteCourseForm(course_id):
    if request.method == 'POST':
        deletedCourse = Courses.query.filter_by(id=course_id).one()
        db.session.delete(deletedCourse)
        flash('%s was Successfully Deleted' % deletedCourse.name)
        db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        if current_user.role_id == 2:   # Only allow access to page if logged in user is a Advisor.
            deletedCourse = Courses.query.filter_by(id=course_id).one()
            return render_template('deleteCourse_form.html', course = deletedCourse)
        else:
            flash('You do not have correct privilege level to access page.')
            return redirect(url_for('creditDashboard'))

# Specific Courses Page
@app.route('/courses/<int:course_id>')
def courseDetail(course_id):
    Course = Courses.query.filter_by(id=course_id).one()
    detail_type = "Course"
    return render_template('course_detail.html', course = Course, button_type = detail_type)

@app.route('/schools')
def schoolDashboard():
    schools = Schools.query.all()
    return render_template('schools_dashboard.html', schools = schools)

@app.route('/schools/<int:school_id>')
def schoolDetail(school_id):
    school = Schools.query.filter_by(id=school_id).one()
    return render_template('school_detail.html', school = school)

@app.route('/degrees')
def degreeDashboard():
    degrees = Degree.query.all()
    return render_template('degrees_dashboard.html', degrees = degrees)

@app.route('/degrees/<int:degree_id>')
def degreeDetail(degree_id):
    degree = Degree.query.filter_by(id=degree_id).one()
    return render_template('degree_detail.html', degree = degree)

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

@app.route('/test/<int:course_id>', methods=['GET', 'POST'])
def test(course_id):
    if request.method == 'POST':
        print('get edit course')
        editedCourse = Courses.query.filter_by(id=course_id).one()
        print(editedCourse)
        print('get multivalue')
        multiselect = request.form.getlist('multival')
        print('Result of multiselect:')
        print(multiselect)
        print(multiselect[0])
        print(multiselect[0].split(','))
        print('Result of multiselect indexes:')
        for coreq_course_id in multiselect[0].split(','):
            print(id)
            print('....')
            coreq_course = Courses.query.filter_by(id=coreq_course_id).one()
            print(coreq_course)
            editedCourse.add_coreq(coreq_course)
            db.session.commit()
        return redirect(url_for('creditDashboard'))
    else:
        editedCourse = Courses.query.filter_by(id=course_id).one()
        depts = Departments.query.all()
        return render_template('test.html', course = editedCourse, depts = depts)
