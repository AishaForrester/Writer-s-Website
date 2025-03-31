from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'new_revision_id'  # Replace with your new revision ID
down_revision = 'b6801ea95adc'  # Use the previous revision ID
branch_labels = None
depends_on = None

def upgrade():
    # Alter the 'user_id' column to be non-nullable
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.alter_column('user_id', nullable=False)

def downgrade():
    # Revert the 'user_id' column to be nullable
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.alter_column('user_id', nullable=True)
