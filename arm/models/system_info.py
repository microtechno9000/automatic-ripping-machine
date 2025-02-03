from models.arm_models import ARMModel
from models.db_setup import db


class SystemInfo(ARMModel):
    """
    ARM Database Model - System Information

    This class holds details about the system (server), including system ID,
    name, CPU, description, and total memory.

    Database Table:
        system_info

    Attributes:
        id (int): The unique identifier for the system information.
        name (str): The name of the system.
        cpu (str): CPU information of the system.
        description (str): Description of the system.
        mem_total (float): Total memory of the system.

    Relationships:
        None
    """
    __tablename__ = 'system_info'

    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Unicode(200))
    ip_address = db.Column(db.String(16))
    port = db.Column(db.Integer)
    arm_type = db.Column(db.String(15))
    # CPU info
    cpu = db.Column(db.String(20))
    cpu_usage = db.Column(db.Float)
    cpu_temp = db.Column(db.Float)
    # Memory / RAM details
    mem_total = db.Column(db.Float())
    mem_available = db.Column(db.Float())
    mem_used = db.Column(db.Float())
    mem_percent = db.Column(db.Float())
    # Storage - configuration files
    storage_config_available = db.Column(db.Float())
    storage_config_used = db.Column(db.Float())
    storage_config_percent = db.Column(db.Float())
    # Storage - transcode files
    storage_transcode_available = db.Column(db.Float())
    storage_transcode_used = db.Column(db.Float())
    storage_transcode_percent = db.Column(db.Float())
    # Storage - completed files
    storage_completed_available = db.Column(db.Float())
    storage_completed_used = db.Column(db.Float())
    storage_completed_percent = db.Column(db.Float())
    # Graphics card status
    hardware_intel = db.Column(db.Boolean)
    hardware_nvidia = db.Column(db.Boolean)
    hardware_amd = db.Column(db.Boolean)
    # Last update
    last_update_time = db.Column(db.DateTime)

    def __init__(self, name: str = "ARM Server", description: str = "Automatic Ripping Machine (ARM) server"):
        self.name = name
        self.description = description
