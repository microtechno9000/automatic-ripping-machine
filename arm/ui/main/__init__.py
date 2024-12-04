from flask import Blueprint

route_main = Blueprint('main',
                       __name__,
                       template_folder='templates',
                       static_folder='../static')

from ui.main import routes  # noqa: E402, F401
