from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Programs, Base, Courses, Departments

engine = create_engine('sqlite:///coursecatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Database entries for new categories or movies.
dept1 = Departments(code="CET", name="Comp Eng")

session.add(dept1)
session.commit()

dept2 = Departments(code="EMT", name="Electromech Eng")

session.add(dept2)
session.commit()

program1 = Courses(name="EMT 1111")

session.add(program1)
session.commit()

program2 = Courses(name="CET 3645")

session.add(program2)
session.commit()


print "added items!"
