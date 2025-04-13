"""
ARM UI Test - Models

Model:
    UI Settings

Tests:
    setup_test_data - Fixture for setting up test data
    test_create_ui_settings - Test creating a new UI Settings record
    test_query_ui_settings - Test querying an existing UI Settings record
"""
import pytest

from models.db_setup import db
from models.ui_settings import UISettings  # Model under test


@pytest.fixture
def setup_test_data():
    """ Fixture for setting up UISettings test data """
    # Get UI Settings from DB
    ui_settings = UISettings.query.first()

    yield ui_settings  # Allow test execution to proceed

    # Clean up (rollback changes)
    db.session.rollback()


def test_query_ui_settings(setup_test_data):
    """ Test querying an existing UISettings record """
    # Check existing data
    ui_settings = UISettings.query.first()
    assert ui_settings is not None

    # Modify data
    ui_settings = UISettings(True,
                             True,
                             "dark",
                             "en",
                             3000,
                             100,
                             5000)

    db.session.add(ui_settings)
    db.session.commit()

    # Assert for values retrieved from the database
    assert ui_settings is not None
    assert ui_settings.use_icons is True
    assert ui_settings.save_remote_images is True
    assert ui_settings.bootstrap_skin == "dark"
    assert ui_settings.language == "en"
    assert ui_settings.index_refresh == 3000
    assert ui_settings.database_limit == 100
    assert ui_settings.notify_refresh == 5000
