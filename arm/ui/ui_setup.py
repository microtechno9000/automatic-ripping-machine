"""
Automatic Ripping Machine - User Interface (UI)
    UI Flask reference module loader
"""
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager

# Initialise Flask Migrations
migrate = Migrate()

# Initialise Cross-Site Request Forgery Protection
csrf = CSRFProtect()

# Initialise the login manager
login_manager = LoginManager()
