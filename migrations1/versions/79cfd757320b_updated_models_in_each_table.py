"""Updated models in each table

Revision ID: 79cfd757320b
Revises: 
Create Date: 2018-03-27 21:46:35.788352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79cfd757320b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=8), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('programs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=8), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('degree', sa.String(length=50), nullable=False),
    sa.Column('dept_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dept_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coreq',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_code', sa.String(length=8), nullable=False),
    sa.Column('coreq_code', sa.String(length=8), nullable=False),
    sa.Column('prog_id', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['prog_id'], ['programs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('code', sa.String(length=8), nullable=False),
    sa.Column('credits', sa.Integer(), nullable=False),
    sa.Column('dept_id', sa.Integer(), nullable=True),
    sa.Column('progs_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dept_id'], ['departments.id'], ),
    sa.ForeignKeyConstraint(['progs_id'], ['programs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prereq',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_code', sa.String(length=8), nullable=False),
    sa.Column('prereq_code', sa.String(length=8), nullable=False),
    sa.Column('prog_id', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['prog_id'], ['programs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prereq')
    op.drop_table('courses')
    op.drop_table('coreq')
    op.drop_table('programs')
    op.drop_table('departments')
    # ### end Alembic commands ###
