"""empty message

Revision ID: b77ad2bae8de
Revises: 29f28dc7cb60
Create Date: 2016-05-27 14:02:22.332953

"""

# revision identifiers, used by Alembic.
revision = 'b77ad2bae8de'
down_revision = '29f28dc7cb60'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('failed_installs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('error_description', sa.String(), nullable=True),
    sa.Column('error_cause', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_system_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('failed_installs')
    ### end Alembic commands ###