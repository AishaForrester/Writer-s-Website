from alembic import op
import sqlalchemy as sa

# Define the revision identifiers, used by Alembic
revision = 'f647ebbd6d85'
down_revision = '23708a1837ad'
branch_labels = None
depends_on = None

def upgrade():
    # Drop the old table if it exists
    op.drop_table('create_books')

    # Recreate the table with the updated schema
    op.create_table(
        'create_books',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(length=120), nullable=True),
        sa.Column('synopsis', sa.String(length=500), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('genre', sa.String(length=50), nullable=True),
        sa.Column('image', sa.String(length=255), nullable=True)
    )

def downgrade():
    # If you need to downgrade, you would drop the new table and recreate the old one
    op.drop_table('create_books')
    op.create_table(
        'create_books',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('synopsis', sa.String(length=200), nullable=True),
        sa.Column('price', sa.String(length=200), nullable=True),
        sa.Column('genre', sa.String(length=50), nullable=True),
        sa.Column('image', sa.String(length=255), nullable=True)
    )
