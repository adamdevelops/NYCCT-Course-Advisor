from app import app, db
from app.models import Departments, Programs, Courses, User, Role


# Clear database first
db.reflect()
db.drop_all()

# Create tables
db.create_all()
db.session.commit()

# Database entries for new categories or movies.
dept1 = Departments(code="CET", name="Comp Eng")

db.session.add(dept1)
db.session.commit()

dept2 = Departments(code="EMT", name="Electromech Eng")

db.session.add(dept2)
db.session.commit()

course1 = Courses(name="EMT 1111", code="EMT", credits=3, dept=dept2)

db.session.add(course1)
db.session.commit()

course2 = Courses(name="CET 3645", code="CET", credits=3, dept=dept1)

db.session.add(course2)
db.session.commit()

course3 = Courses(name="EMT 1250", code="EMT", credits=3, dept=dept2)

# db.session.add(course3)
# db.session.commit()

# Courses('node1_EMT1120', parent=course3)
# db.session.add(course3)
# db.session.commit()

course4 = Courses(name="EMT 1120", code="EMT", credits=3, dept=dept2)

db.session.add(course4)
db.session.commit()

program1 = Programs(code="EMT", name="Electro-Mechanical Engineering Technology", degree='AAS', dept=dept2)

db.session.add(program1)
db.session.commit()

program2 = Programs(code="EMT", name="Electro-Mechanical Engineering Technology", degree='AAS', dept=dept1)

db.session.add(program1)
db.session.commit()



# prereq1 = Prereq(course_code="EM1250", prereq_code="EMT1120")
#
# db.session.add(prereq1)
# db.session.commit()

# coreq1 = Coreq(course_code="EM1150", coreq_code="MAT1175")
#
# db.session.add(coreq1)
# db.session.commit()

print ("added items!")

######################
# Query for departments with EMT code and print courses under that department
dept = Departments.query.filter_by(code='EMT').first()
print (dept)
print (dept.course_depts)
print (dept.course_depts[0].name)

# Display Department for Course1
print(course1.dept.name)

# Add prereq course to Database
course3.add_prereq(course4)
course3.add_prereq(course1)
course2.add_prereq(course3)
course1.add_coreq(course4)
db.session.commit()

print (course3.prereqs)

# Course 3 EMT1250 should have prereqs of EMT1111, EMT1120
# Course 2 CET3645 should have prereqs of EMT1250

def users_roles():
    # Create two main roles Student and Advisor
    stu_role = Role(role_name='Student', description='A student enrolled in the college taking some courses.')
    fac_role = Role(role_name='Advisor',
                    description='An academic advisor, faculty member or staff, that will help student.')
    db.session.add(stu_role)
    db.session.add(fac_role)
    db.session.commit()

    # Create five users, 3 students and 2 advisors
    u1 = User(username='AdamH', email='adam.h@example.com', role=stu_role)
    u2 = User(username='PeterP', email='peter.parker@avengers.com', role=stu_role)
    u3 = User(username='JohnnyS', email='john.smith@example.com', role=stu_role)
    u4 = User(username='Dr.X', email='charles.xavier@avenger.com', role=fac_role)
    u5 = User(username='BenM', email='ben.m@example.com', role=fac_role)
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.add(u4)
    db.session.add(u5)
    db.session.commit()

    # Assigning an advisor to an user
    u1.advisor = u5  # u1.advisor is the relationship and u5 is a User object
    u2.advisor = u4
    u3.advisor_id = u5.id  # Another way to do it is using the advisor_id field directly
    db.session.commit()

# Create users
users_roles()
