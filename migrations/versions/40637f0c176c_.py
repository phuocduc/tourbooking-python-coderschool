"""empty message

Revision ID: 40637f0c176c
Revises: 96230d25f15b
Create Date: 2019-12-12 13:20:44.650109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40637f0c176c'
down_revision = '96230d25f15b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book_tours', sa.Column('image', sa.Text(), nullable=True))
    op.add_column('book_tours', sa.Column('prices', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book_tours', 'prices')
    op.drop_column('book_tours', 'image')
    # ### end Alembic commands ###
