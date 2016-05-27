"""empty message

Revision ID: 29f28dc7cb60
Revises: None
Create Date: 2016-05-27 13:57:56.468970

"""

# revision identifiers, used by Alembic.
revision = '29f28dc7cb60'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_system_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('system_dist', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('system', sa.String(), nullable=True),
    sa.Column('machine', sa.String(), nullable=True),
    sa.Column('system_platform', sa.String(), nullable=True),
    sa.Column('uname', sa.String(), nullable=True),
    sa.Column('python_version', sa.String(), nullable=True),
    sa.Column('workshop_id', sa.String(), nullable=True),
    sa.Column('email_id', sa.String(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('successful_installs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_system_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('successful_installs')
    op.drop_table('user_system_info')
    ### end Alembic commands ###