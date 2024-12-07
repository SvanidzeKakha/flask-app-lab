"""user model added

Revision ID: 09a09ad20ec5
Revises: dd8e6c4396c9
Create Date: 2024-12-06 20:26:29.815479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09a09ad20ec5'
down_revision = 'dd8e6c4396c9'
branch_labels = None
depends_on = None


def upgrade():
    # Create the users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(20), nullable=False),
        sa.Column('email', sa.String(120), unique=True, nullable=False),
        sa.Column('password', sa.String(60), nullable=False),
    )

def downgrade():
    # Drop the users table
    op.drop_table('users')