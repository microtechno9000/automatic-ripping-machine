"""
Automatic Ripping Machine - User Interface (UI)
    Flask factory
"""
from flask import Flask
from flask_cors import CORS

from ui_config import UIConfig
from ui.setuplog import setuplog
from ui.ui_setup import db, migrate, csrf, login_manager


def create_app(config_class=UIConfig):
    # Setup logging
    dictConfig = setuplog(config_class)

    app = Flask(__name__)
    app.config.from_object(config_class)
    csrf.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "False"}})

    # Report system state for debugging
    app.logger.debug("Debugging pin: " + config_class.WERKZEUG_DEBUG_PIN)
    # app.logger.debug("Debugging pin: " + app.config["WERKZEUG_DEBUG_PIN"])
    # app.logger.debug(f"Mysql configuration: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Initialise the Database and Flask Alembic
    db.init_app(app)
    # alembic.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)

    # Register route blueprints
    from ui.ui_blueprints import register_blueprints
    register_blueprints(app)

    return app
