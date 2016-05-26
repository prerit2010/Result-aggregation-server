"""empty message

Revision ID: 127883dd3224
Revises: 6ca86ef1eb15
Create Date: 2016-05-26 23:16:53.667148

"""

# revision identifiers, used by Alembic.
revision = '127883dd3224'
down_revision = '6ca86ef1eb15'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_system_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('system_dist', sa.String(), nullable=True),
    sa.Column('system', sa.String(), nullable=True),
    sa.Column('machine', sa.String(), nullable=True),
    sa.Column('system_platform', sa.String(), nullable=True),
    sa.Column('uname', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('python_version', sa.String(), nullable=True),
    sa.Column('workshop_id', sa.String(), nullable=True),
    sa.Column('email_id', sa.String(), nullable=True),
    sa.Column('Create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_system_info')
    ### end Alembic commands ###