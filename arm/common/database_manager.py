"""
Automatic Ripping Machine (ARM) - Common Files
    Database Manager

Scripts for checking and managing the current state of the database.
"""
from alembic.script import ScriptDirectory
from alembic.config import Config


def get_alembic_version() -> str:
    """
    Get the current alembic version from the ARM migrations folder.
    """
    alembic_config = Config()
    alembic_config.set_main_option("script_location", "/opt/arm/arm/ui/migrations")
    alembic_script = ScriptDirectory.from_config(alembic_config)
    alembic_head = alembic_script.get_current_head()

    return alembic_head
