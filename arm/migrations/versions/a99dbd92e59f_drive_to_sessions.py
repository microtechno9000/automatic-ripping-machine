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
    with op.batch_alter_table('system_drives') as batch_mod:
        batch_mod.add_column(sa.Column('session_id', sa.Integer(), nullable=False))
        batch_mod.create_foreign_key('session_fk_1', 'sessions', ['session_id'], ['id'])


def downgrade():
    op.drop_constraint('session_id_fk_1', 'system_drives', type_='foreignkey')
    # op.drop_column('system_drives', 'session_id')
