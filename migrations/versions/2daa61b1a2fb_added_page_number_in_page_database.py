"""Added page number in Page database

Revision ID: 2daa61b1a2fb
Revises: c820b7605683
Create Date: 2025-03-01 19:28:48.615481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2daa61b1a2fb'
down_revision = 'c820b7605683'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pages', schema=None) as batch_op:
        op.add_column('pages', sa.Column('page_number', sa.Integer(), nullable=True))

        # Set a default value for existing rows
        op.execute("UPDATE pages SET page_number = 1")

        # Now make it NOT NULL
        op.alter_column('pages', 'page_number', nullable=False)


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pages', schema=None) as batch_op:
        batch_op.drop_column('page_number')

    # ### end Alembic commands ###
