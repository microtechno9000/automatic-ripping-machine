"""
ARM Functions for all blueprints

NOTE: Avoid using this unless functions are shared between blueprints

Functions
    - authenticated_state - check if user is authenticated
"""
from flask_login import current_user

import arm.config.config as cfg


def authenticated_state() -> bool:
    """
    Determines whether the current user is considered authenticated.

    This function checks the application's configuration to see if login
    authentication is disabled. If login is disabled, it automatically
    returns `True`, indicating that the user is authenticated. Otherwise,
    it checks the `current_user.is_authenticated` attribute provided by
    Flask-Login to determine if the user is logged in.

    Returns:
        bool: `True` if the user is authenticated, either by bypassing
        the login requirement or by being a logged-in user; `False` otherwise.
    """
    authenticated = False
    if cfg.arm_config['DISABLE_LOGIN']:
        authenticated = True
    else:
        if current_user.is_authenticated:
            authenticated = True

    return authenticated
