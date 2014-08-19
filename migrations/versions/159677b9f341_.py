"""empty message

Revision ID: 159677b9f341
Revises: 61e76eae142
Create Date: 2014-08-18 19:54:25.002000

"""

# revision identifiers, used by Alembic.
revision = '159677b9f341'
down_revision = '61e76eae142'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profile_image', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'profile_image')
    ### end Alembic commands ###