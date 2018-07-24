from app import app, db
from app.models import Departments, Programs, Courses, Prereq, Coreq


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

course1 = Courses(name="EMT 1111", code="EMT", credits=3)

db.session.add(course1)
db.session.commit()

course2 = Courses(name="CET 3645", code="EMT", credits=3)

db.session.add(course2)
db.session.commit()

program1 = Programs(code="EMT", name="Electro-Mechanical Engineering Technology", degree='AAS', departments=dept2)

db.session.add(program1)
db.session.commit()

prereq1 = Prereq(course_code="EM1220", prereq_code="EMT1120")

db.session.add(prereq1)
db.session.commit()

coreq1 = Coreq(course_code="EM1150", coreq_code="MAT1175")

db.session.add(coreq1)
db.session.commit()

print ("added items!")

######################
# Adding EMT1111 course to EMT department via association table
course1.course_department.append(dept2)

# Printing Department that the course was assigned to
for dep in course1.course_department:
    print (dep.name)
    print (dep.code)
    print (dep.id)
