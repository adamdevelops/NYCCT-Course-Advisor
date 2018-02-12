from app import app, db
from app.models import Departments, Programs

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Departments': Departments, 'Programs': Programs}
