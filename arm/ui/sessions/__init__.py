"""
ARM route blueprint for sessions pages
"""
from flask import Blueprint

route_sessions = Blueprint('route_sessions', __name__,
                           template_folder='templates',
                           static_folder='../static')

from arm.ui.sessions import routes  # noqa: E402, F401
