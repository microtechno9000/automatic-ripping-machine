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
    config_instance = config_class()

    # Setup logging
    dictConfig(setuplog(config_instance.LOG_PATH,
                        config_instance.LOG_SIZE,
                        config_instance.LOG_COUNT,
                        ))

    # Start Flask Web Server
    app = Flask(__name__)

    # Flask application configuration
    app.config.from_object(config_instance)
    csrf.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "False"}})

    # Set log level per arm.yml config
    app.logger.debug(f"Starting Flask app: {__name__}")
    app.logger.info(f"Setting log level to: {config_instance.LOGLEVEL}")
    app.logger.setLevel(config_instance.LOGLEVEL)
    app.logger.debug(f"Logging file: {config_instance.LOG_PATH}"
                     f" max size: {config_instance.LOG_SIZE}"
                     f" log count: {config_instance.LOG_COUNT}")

    # Report system state for debugging
    app.logger.debug(f'Starting ARM in [{config_instance.ENV}] mode')
    app.logger.debug(f'Starting FLASK in debug: {config_instance.FLASK_DEBUG}')
    app.logger.debug(f'Debugging pin: {config_instance.WERKZEUG_DEBUG_PIN}')
    app.logger.debug(f'Mysql configuration: {config_instance.mysql_uri_sanitised}')
    app.logger.debug(f'SQLite Configuration: {config_instance.sqlitefile}')
    app.logger.debug(f'Login Disabled: {config_instance.LOGIN_DISABLED}')
    if config_instance.DOCKER:
        app.logger.info('ARM UI Running within Docker, ignoring any config in arm.yml')
    app.logger.info(f'Starting ARM UI on interface address - {config_instance.SERVER_HOST}:{config_instance.SERVER_PORT}')

    # Pause ARM to ensure ARM DB is up and running
    if config_instance.DOCKER and config_instance.ENV != 'development':
        app.logger.info("Sleeping for 60 seconds to ensure ARM DB is active")
        sleep(55)
        for i in range(5, 0, -1):
            app.logger.info(f"Starting in ... {i}")
            sleep(1)
        app.logger.info("Starting ARM")

    # Initialise connection to databases
    db.init_app(app)  # Initialise database
    app.logger.debug(f'Alembic Migration Folder: {config_instance.alembic_migrations_dir}')
    migrate.init_app(app, db, directory=config_instance.alembic_migrations_dir)

    with app.app_context():
        # # Upgrade or load the ARM database to the latest head/version
        upgrade(directory=config_instance.alembic_migrations_dir,
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
        if not config_instance.TESTING:
            initialise_arm(app, db)

    # Remove GET/page loads from logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    return app
