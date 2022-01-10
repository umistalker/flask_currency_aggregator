"""empty message

Revision ID: f0a77048714b
Revises: c0955a9503e6
Create Date: 2022-01-08 09:31:40.212488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0a77048714b'
down_revision = 'c0955a9503e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('xrate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_currency', sa.Integer(), nullable=True),
    sa.Column('to_currency', sa.DECIMAL(), nullable=True),
    sa.Column('rate', sa.Float(), nullable=True),
    sa.Column('updated', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('xrate')
    # ### end Alembic commands ###