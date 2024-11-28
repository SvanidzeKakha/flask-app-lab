"""add is_active, category and author

Revision ID: 15f797438ad8
Revises: dd762264c6e1
Create Date: 2024-11-28 22:03:04.301518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15f797438ad8'
down_revision = 'dd762264c6e1'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('posts') as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=100), nullable=False, server_default='General'))
        batch_op.add_column(sa.Column('author', sa.String(length=100), nullable=False, server_default='Unknown'))
    
    # Remove default after upgrade, if unnecessary
    op.alter_column('posts', 'category', server_default=None)
    op.alter_column('posts', 'author', server_default=None)
    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('posts') as batch_op:
        batch_op.drop_column('category')
        batch_op.drop_column('author')

    # ### end Alembic commands ###
