"""empty message

Revision ID: 3876d7949797
Revises: 43a38e4e334d
Create Date: 2015-06-14 00:00:52.527536

"""

# revision identifiers, used by Alembic.
revision = '3876d7949797'
down_revision = '43a38e4e334d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person', sa.Column('isAdmin', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('person', 'isAdmin')
    ### end Alembic commands ###
