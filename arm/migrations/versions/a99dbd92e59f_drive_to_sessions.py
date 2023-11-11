"""drive to sessions

Revision ID: a99dbd92e59f
Revises: 352b86a5fb63
Create Date: 2023-11-08 21:53:45.003007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a99dbd92e59f'
down_revision = '352b86a5fb63'
branch_labels = None
depends_on = None


def upgrade():
    """
    add column to system_drives table, linking any current sessions to the session table
    """
    op.add_column('system_drives',
                  sa.Column('session_id', sa.Integer(), sa.ForeignKey('sessions.id')),
                  # sa.ForeignKeyConstraint(('session_id',), ['sessions.id'],),
                  )
    # op.create_foreign_key('session_id', 'system_drives', 'sessions', ['session_id'], ['id'])
#     fix - https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.create_foreign_key


def downgrade():
    op.drop_column('system_drives', 'session_id')
