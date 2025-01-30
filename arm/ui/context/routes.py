"""
Automatic Ripping Machine - User Interface (UI) - Blueprint
    Context

    Provides Flask Context Processor
"""
from flask import render_template

from flask import current_app as app
from arm.models.ui_settings import UISettings


@app.context_processor
def inject_arm_cfg():
    """
    ARM context processor
    Inject ARM config bootstrap skin settings into all flask context
    """
    try:
        armui_cfg = UISettings.query.filter_by().first()
    except Exception as error:
        return render_template('error.html', error=error)

    return dict(bootstrap_skin=armui_cfg.bootstrap_skin)
