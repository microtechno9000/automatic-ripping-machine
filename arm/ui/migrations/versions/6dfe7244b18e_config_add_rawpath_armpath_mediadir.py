"""

Revision ID: 6dfe7244b18e
Revises: 9cae4aa05dd7
Create Date: 2021-03-19 19:22:53.502215

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6dfe7244b18e'
down_revision = '9cae4aa05dd7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(table_name="config",
                    column_name="RAWPATH",
                    existing_type=sa.String(length=255),
                    existing_nullable=True,
                    new_column_name="RAW_PATH")
    op.alter_column(table_name="config",
                    column_name="ARMPATH",
                    existing_type=sa.String(length=255),
                    existing_nullable=True,
                    new_column_name="TRANSCODE_PATH")
    op.alter_column(table_name="config",
                    column_name="MEDIA_DIR",
                    existing_type=sa.String(length=255),
                    existing_nullable=True,
                    new_column_name="COMPLETED_PATH")


def downgrade():
    op.alter_column("config",
                    "RAW_PATH",
                    new_column_name="RAWPATH")
    op.alter_column("config",
                    "TRANSCODE_PATH",
                    new_column_name="ARMPATH")
    op.alter_column("config",
                    "COMPLETED_PATH",
                    new_column_name="MEDIA_DIR")
