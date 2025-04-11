"""
Automatic Ripping Machine - User Interface (UI)
    Flask factory
"""
import os
from time import sleep
from flask import Flask
from flask_cors import CORS
from flask_migrate import upgrade
import logging
from logging.config import dictConfig

from ui.setuplog import setuplog
from ui.ui_initialise import initialise_arm
from models.db_setup import db
from ui.ui_setup import migrate, csrf, login_manager
from ui_config import config_classes


def create_app(config_name=os.getenv("FLASK_ENV", "production")):
    """
    Flask Application Factory
    """
    # Define the ui_config class
    config_class = config_classes.get(config_name.lower())

    # Setup logging
    # TODO: change these to a database config for user config
    log_filename: str = "/arm/logs/arm_ui.log"
    log_size = 5
    log_count = 2
    dictConfig(setuplog(log_filename, log_size, log_count))

    app = Flask(__name__)

    # Flask application configuration
    app.config.from_object(config_class)
    csrf.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "False"}})

    # Set log level per arm.yml config
    app.logger.debug(f"Starting Flask app: {__name__}")
    app.logger.info(f"Setting log level to: {config_class.LOGLEVEL}")
    app.logger.setLevel(config_class.LOGLEVEL)

    # Report system state for debugging
    app.logger.debug(f'Starting ARM in [{config_class.ENV}] mode')
    app.logger.debug(f'Starting FLASK in debug: {app.config["FLASK_DEBUG"]}')
    app.logger.debug(f'Debugging pin: {app.config["WERKZEUG_DEBUG_PIN"]}')
    app.logger.debug(f'Mysql configuration: {config_class.mysql_uri_sanitised}')
    app.logger.debug(f'SQLite Configuration: {config_class.sqlitefile}')
    app.logger.debug(f'Login Disabled: {app.config["LOGIN_DISABLED"]}')
    if config_class.DOCKER:
        app.logger.info('ARM UI Running within Docker, ignoring any config in arm.yml')
    app.logger.info(f'Starting ARM UI on interface address - {app.config["SERVER_HOST"]}:{app.config["SERVER_PORT"]}')

    # Pause ARM to ensure ARM DB is up and running
    if config_class.DOCKER and config_class.ENV != 'development':
        app.logger.info("Sleeping for 60 seconds to ensure ARM DB is active")
        sleep(55)
        for i in range(5, 0, -1):
            app.logger.info(f"Starting in ... {i}")
            sleep(1)
        app.logger.info("Starting ARM")

    # Initialise connection to databases
    db.init_app(app)  # Initialise database
    app.logger.debug(f'Alembic Migration Folder: {config_class.alembic_migrations_dir}')
    migrate.init_app(app, db, directory=config_class.alembic_migrations_dir)

    with app.app_context():
        # # Upgrade or load the ARM database to the latest head/version
        upgrade(directory=config_class.alembic_migrations_dir,
                revision='head')

        # Initialise the Flask-Login manager
        login_manager.init_app(app)

        # Register route blueprints
        from ui.ui_blueprints import register_blueprints
        register_blueprints(app)

        # Register auth user and handler
        from ui.auth.routes import load_user, unauthorized
        login_manager.user_loader(load_user)
        login_manager.unauthorized_handler(unauthorized)

        # Initialise ARM and ensure tables are set, when not in Test
        if not config_class.TESTING:
            initialise_arm(app, db)

    # Remove GET/page loads from logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    return app
