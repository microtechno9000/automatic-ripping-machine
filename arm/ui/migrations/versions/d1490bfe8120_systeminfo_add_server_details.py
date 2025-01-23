"""
Addition of ARM Ripper server IP and Port details to a database

Revision ID: d1490bfe8120
Revises: 7aaf1ab1fe07
Create Date: 2025-01-21 12:51:49.345646

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd1490bfe8120'
down_revision = '7aaf1ab1fe07'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('system_info',
                  sa.Column('ip_address', sa.String(length=16))
                  )
    op.add_column('system_info',
                  sa.Column('port', sa.Integer())
                  )
    op.add_column('system_info',
                  sa.Column('arm_type', sa.String(length=15))
                  )
    op.add_column('system_info',
                  sa.Column('cpu_usage', sa.Float())
                  )
    op.add_column('system_info',
                  sa.Column('cpu_temp', sa.Float())
                  )
    op.add_column('system_info',
                  sa.Column('mem_available', sa.Float())
                  )
    op.add_column('system_info',
                  sa.Column('mem_used', sa.Float())
                  )
    op.add_column('system_info',
                  sa.Column('mem_percent', sa.Float())
                  )


def downgrade():
    op.drop_column('system_info', 'ip_address')
    op.drop_column('system_info', 'port')
    op.drop_column('system_info', 'arm_type')
    op.drop_column('system_info', 'cpu_usage')
    op.drop_column('system_info', 'cpu_temp')
    op.drop_column('system_info', 'mem_available')
    op.drop_column('system_info', 'mem_used')
    op.drop_column('system_info', 'mem_percent')
