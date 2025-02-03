"""
Automatic Ripping Machine (ARM) - Ripper Monitor

This script runs as a background process, generating system information for the running ripper docker container.
Once running, will push current system information to the ARM database for the UI to access and status

This script is not for monitoring jobs, just the status of the ripper docker container
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from time import sleep
from datetime import datetime

from ripper.monitor.MonitorConfig import MonitorConfig
from ripper.monitor.LoggerConfig import setup_logging
from common.database_manager import get_alembic_version
from common.ServerDetails import ServerDetails
from common.server_ip import detect_ip
from models.alembic_version import AlembicVersion
from models.system_info import SystemInfo
from models.db_setup import db


if __name__ == '__main__':
    # Configure the Monitor
    config = MonitorConfig()
    # Setup Logging
    logger = setup_logging(config)
    system_ip = detect_ip()
    logger.debug(f"System IP Address: {system_ip}")
    # Set up the database
    engine = create_engine(config.mysql_uri)
    db.Model.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check database is current before monitoring
    while True:
        # Refresh the session cache
        # session.expire_all()
        alembic_version = get_alembic_version()
        database_version = session.query(AlembicVersion).first()
        logger.debug(f"Alembic Version: {alembic_version} Database Version: {database_version.version_num}")

        if database_version.version_num == alembic_version:
            break  # Exit loop if current

        logger.info("Alembic Version does not match database version. Waiting 60 seconds then checking again")
        session.close()
        sleep(60)

    # Check if ripper details exist
    server_ripper = session.query(SystemInfo).filter_by(arm_type="ripper",
                                                        ip_address=system_ip).first()
    # Load system status
    server_details = ServerDetails()

    # Ripper doesn't exist in the database, create new entry
    if server_ripper is None:
        logger.info("Adding ripper into database")
        server_ripper = SystemInfo(name="ARM Ripper",
                                   description="Separate ARM Ripper container")
        server_ripper.ip_address = system_ip
        server_ripper.port = 8080
        server_ripper.arm_type = "ripper"
        # CPU Details
        server_ripper.cpu = server_details.cpu
        server_ripper.cpu_usage = server_details.cpu_util
        server_ripper.cpu_temp = server_details.cpu_temp
        # Memory Details
        server_ripper.mem_total = server_details.mem_total
        server_ripper.mem_available = server_details.memory_free
        server_ripper.mem_used = server_details.memory_used
        server_ripper.mem_percent = server_details.memory_percent
        # Storage Info
        server_ripper.storage_config_available = 0
        server_ripper.storage_config_used = 0
        server_ripper.storage_config_percent = 0
        server_ripper.storage_transcode_available = server_details.storage_transcode_free
        server_ripper.storage_transcode_used = 0
        server_ripper.storage_transcode_percent = server_details.storage_transcode_percent
        server_ripper.storage_completed_available = server_details.storage_completed_free
        server_ripper.storage_completed_used = 0
        server_ripper.storage_completed_percent = server_details.storage_completed_percent
        # Graphics card info
        server_ripper.hardware_intel = False
        server_ripper.hardware_nvidia = False
        server_ripper.hardware_amd = False
        # Last update time
        server_ripper.last_update_time = datetime.now()
        session.add(server_ripper)
        session.commit()

        logger.debug("*" * 40)
        logger.debug(f"Name: {server_ripper.name}")
        logger.debug(f"Description: {server_ripper.description}")
        logger.debug(f"CPU: {server_ripper.cpu}")
        logger.debug(f"ARM Type: {server_ripper.arm_type}")
        logger.debug(f"Last Update Time: {server_ripper.last_update_time}")
        logger.debug("*" * 40)

    string_padding = 18
    value_padding = 5

    # Update system usage
    while True:
        server_details.get_update()
        server_ripper.cpu_usage = server_details.cpu_util
        server_ripper.cpu_temp = server_details.cpu_temp
        server_ripper.mem_total = server_details.mem_total
        server_ripper.mem_available = server_details.memory_free
        server_ripper.mem_used = server_details.memory_used
        server_ripper.mem_percent = server_details.memory_percent
        # Update storage
        server_ripper.storage_config_available = 0
        server_ripper.storage_config_used = 0
        server_ripper.storage_config_percent = 0
        server_ripper.storage_transcode_available = server_details.storage_transcode_free
        server_ripper.storage_transcode_used = 0
        server_ripper.storage_transcode_percent = server_details.storage_transcode_percent
        server_ripper.storage_completed_available = server_details.storage_completed_free
        server_ripper.storage_completed_used = 0
        server_ripper.storage_completed_percent = server_details.storage_completed_percent
        server_ripper.last_update_time = datetime.now()
        session.add(server_ripper)
        session.commit()
        logger.debug("*" * 40)
        logger.debug(f"{'CPU Usage:':<{string_padding}} {server_ripper.cpu_usage:>{value_padding}.2f} %")
        logger.debug(f"{'CPU Temperature:':<{string_padding}} {server_ripper.cpu_temp:>{value_padding}.2f}°C")
        logger.debug(f"{'Memory Total:':<{string_padding}} {server_ripper.mem_total:>{value_padding}.2f} GB")
        logger.debug(f"{'Memory Available:':<{string_padding}} {server_ripper.mem_available:>{value_padding}.2f} GB")
        logger.debug(f"{'Memory Used:':<{string_padding}} {server_ripper.mem_used:>{value_padding}.2f} GB")
        logger.debug(f"{'Memory Percent:':<{string_padding}} {server_ripper.mem_percent:>{value_padding}.2f} %")
        logger.info(f"{'Last Update Time:':<{string_padding}} "
                    f"{server_ripper.last_update_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.debug("*" * 40)
        sleep(60)
