"""
ARM UI Test - Models

Model:
    System Info

Tests:
    setup_test_data - Fixture for setting up test data
    test_create_system_info - Test creating a new System Info record
    test_query_system_info - Test querying an existing System Info record
"""
import pytest
import datetime

from models.db_setup import db
from models.system_info import SystemInfo       # Model under test


@pytest.fixture
def setup_test_data():
    """ Fixture for setting up test data """
    # Create a sample SystemInfo instance for testing
    system_info = SystemInfo("Test Server",
                             "Test server description")
    # Set additional fields
    system_info.ip_address = "192.168.1.100"
    system_info.port = 8080
    system_info.arm_type = "docker"

    # CPU info
    system_info.cpu = "Phenom X4 9850 Black Edition"
    system_info.cpu_usage = 27.5
    system_info.cpu_temp = 60.3

    # Memory info
    system_info.mem_total = 24.0
    system_info.mem_available = 12.5
    system_info.mem_used = 11.5
    system_info.mem_percent = 47.9

    # Storage - config
    system_info.storage_config_available = 50.0
    system_info.storage_config_used = 10.0
    system_info.storage_config_percent = 20.0

    # Storage - transcode
    system_info.storage_transcode_available = 200.0
    system_info.storage_transcode_used = 80.0
    system_info.storage_transcode_percent = 40.0

    # Storage - completed
    system_info.storage_completed_available = 500.0
    system_info.storage_completed_used = 100.0
    system_info.storage_completed_percent = 20.0

    # Hardware detection
    system_info.hardware_intel = True
    system_info.hardware_nvidia = False
    system_info.hardware_amd = False

    # Last update
    system_info.last_update_time = datetime.datetime.utcnow()

    db.session.add(system_info)
    db.session.commit()

    yield system_info  # Allow test execution to proceed

    # Clean up (rollback changes)
    db.session.rollback()


def test_create_system_info(setup_test_data):
    """ Test creating a new SystemInfo record """
    # Create a sample SystemInfo instance for testing
    system_info = SystemInfo("Test Server",
                             "Test server description")
    system_info.cpu = "Phenom X4 9850 Black Edition"
    system_info.mem_total = "24.0"
    db.session.add(system_info)
    db.session.commit()

    # Ensure the record exists
    assert system_info.id is not None


def test_query_system_info(setup_test_data):
    """ Test querying an existing SystemInfo record """
    system_info = SystemInfo.query.first()

    # Assert for values retrieved from the database
    assert system_info is not None
    assert system_info.name == "Test Server"
    assert system_info.description == "Test server description"
    assert system_info.ip_address == "192.168.1.100"
    assert system_info.port == 8080
    assert system_info.arm_type == "docker"

    assert system_info.cpu == "Phenom X4 9850 Black Edition"
    assert system_info.cpu_usage == 27.5
    assert system_info.cpu_temp == 60.3

    assert system_info.mem_total == 24.0
    assert system_info.mem_available == 12.5
    assert system_info.mem_used == 11.5
    assert system_info.mem_percent == 47.9

    assert system_info.storage_config_available == 50.0
    assert system_info.storage_config_used == 10.0
    assert system_info.storage_config_percent == 20.0

    assert system_info.storage_transcode_available == 200.0
    assert system_info.storage_transcode_used == 80.0
    assert system_info.storage_transcode_percent == 40.0

    assert system_info.storage_completed_available == 500.0
    assert system_info.storage_completed_used == 100.0
    assert system_info.storage_completed_percent == 20.0

    assert system_info.hardware_intel is True
    assert system_info.hardware_nvidia is False
    assert system_info.hardware_amd is False

    assert system_info.last_update_time is not None
