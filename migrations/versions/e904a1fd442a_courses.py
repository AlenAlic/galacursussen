"""courses

Revision ID: e904a1fd442a
Revises: a33eb2f4b555
Create Date: 2019-08-19 18:02:01.047240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e904a1fd442a'
down_revision = 'a33eb2f4b555'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('requested_by', sa.String(length=256), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.Interval(), nullable=True),
    sa.Column('attendees', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=256), nullable=True),
    sa.Column('language', sa.Enum('nl', 'en', 'unknown', name='language'), nullable=False),
    sa.Column('committee', sa.Enum('incie', 'salcie', name='committee'), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=False),
    sa.Column('dances', sa.String(length=256), nullable=True),
    sa.Column('notes', sa.String(length=256), nullable=True),
    sa.Column('cancelled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('course_id')
    )
    op.create_table('assignment',
    sa.Column('assignment_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('mucie', sa.Boolean(), nullable=False),
    sa.Column('teacher', sa.Boolean(), nullable=False),
    sa.Column('assistant', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('assignment_id')
    )
    op.create_table('assignment_request',
    sa.Column('assignment_request_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('attendance', sa.Enum('yes', 'maybe', 'no', name='attendance'), nullable=True),
    sa.Column('notes', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('assignment_request_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assignment_request')
    op.drop_table('assignment')
    op.drop_table('course')
    # ### end Alembic commands ###
