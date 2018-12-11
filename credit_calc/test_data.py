from app import app, db
from app.models import Departments, Programs, Courses


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

db.session.add(course3)
db.session.commit()

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

# Course 3 EMT1250 should have prereqs of EMT1111, EMT1120
# Course 2 CET3645 should have prereqs of EMT1250
