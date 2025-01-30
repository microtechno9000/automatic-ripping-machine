"""
Automatic Ripping Machine - User Interface (UI) - Blueprint
    Middleware

    This class is called prior to loading any routes
"""
from flask import render_template

from arm.models.ui_settings import UISettings


class Middleware():
    """
    ARM Middleware class

    Loads the ARM UI Config from DB
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Set UI Config values for cookies
        # the database should be available and data loaded by this point
        try:
            self.armui_cfg = UISettings.query.filter_by().first()
        except Exception as error:
            return render_template('error.html', error=error)

        # Set environment variable
        environ['armui_skin'] = self.armui_cfg.bootstrap_skin
        return self.app(environ, start_response)
