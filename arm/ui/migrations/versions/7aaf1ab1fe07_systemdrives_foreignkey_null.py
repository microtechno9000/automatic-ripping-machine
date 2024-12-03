"""
system_drives allow foreign key to be nullable in mysql
Required as mysql is not forgiving

Revision ID: 7aaf1ab1fe07
Revises: bae285cef5a8
Create Date: 2024-11-27 20:45:11.644206

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7aaf1ab1fe07'
down_revision = 'bae285cef5a8'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the foreign key constraints
    op.drop_constraint('system_drives_ibfk_1',
                       'system_drives',
                       type_='foreignkey')
    op.drop_constraint('system_drives_ibfk_2',
                       'system_drives',
                       type_='foreignkey')

    # Alter the columns to allow NULL values
    op.alter_column('system_drives', 'job_id_current',
                    existing_type=sa.Integer,
                    nullable=True)
    op.alter_column('system_drives', 'job_id_previous',
                    existing_type=sa.Integer,
                    nullable=True)

    # Recreate the foreign key constraints
    op.create_foreign_key('system_drives_ibfk_1',
                          'system_drives',
                          'job',
                          ['job_id_current'],
                          ['job_id'])
    op.create_foreign_key('system_drives_ibfk_2',
                          'system_drives',
                          'job',
                          ['job_id_previous'],
                          ['job_id'])


def downgrade():
    # Drop the foreign key constraints temporarily
    op.drop_constraint('system_drives_ibfk_1',
                       'system_drives',
                       type_='foreignkey')
    op.drop_constraint('system_drives_ibfk_2',
                       'system_drives',
                       type_='foreignkey')

    # Alter the columns to disallow NULL values
    op.alter_column('system_drives',
                    'job_id_current',
                    existing_type=sa.Integer,
                    nullable=False)
    op.alter_column('system_drives',
                    'job_id_previous',
                    existing_type=sa.Integer,
                    nullable=False)

    # Recreate the foreign key constraints
    op.create_foreign_key('system_drives_ibfk_1',
                          'system_drives',
                          'job',
                          ['job_id_current'],
                          ['job_id'])
    op.create_foreign_key('system_drives_ibfk_2',
                          'system_drives',
                          'job',
                          ['job_id_previous'],
                          ['job_id'])

