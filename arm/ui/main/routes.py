"""
Automatic Ripping Machine - User Interface (UI) - Blueprint
    Main

Covers
    - index [GET]
    - dbupdate [POST]
"""
import flask
from flask import current_app
from flask import render_template, session, redirect
from flask_login import login_required

from flask import current_app as app
import config.config as cfg
import ui.ui_utils as ui_utils
from ui.main import route_main
from models.db_setup import db
from ui.main.forms import SystemInfoLoad
from common.ServerDetails import ServerDetails
from ui.settings.utils import check_hw_transcode_support
from models.system_info import SystemInfo


@route_main.route('/')
@route_main.route('/index.html')
@route_main.route('/index')
def home():
    """
    The main homepage showing current rips and server stats
    """
    # Check if system info is populated, otherwise go to system setup
    arm_ui = SystemInfo.query.filter_by(arm_type="ui").first()
    if not arm_ui:
        return redirect('/systemsetup')

    # Load each of the ARM Server details
    arm_servers = SystemInfo.query.filter_by().all()

    # Push out HW transcode status for homepage
    stats = {'hw_support': check_hw_transcode_support()}

    # System details in class server
    arm_path = cfg.arm_config['TRANSCODE_PATH']
    media_path = cfg.arm_config['COMPLETED_PATH']

    # Page titles
    session["arm_name"] = cfg.arm_config['ARM_NAME']
    session["page_title"] = "Home"

    # TODO fix this back to something that works, pending ripper working
    jobs = {}

    # Set authentication state for index
    authenticated = ui_utils.authenticated_state()
    current_app.logger.debug(f'Authentication state: {authenticated}')

    # response = flask.make_response()
    # response.set_cookie("index_refresh", value=f"{armui_cfg.index_refresh}")
    return render_template("index.html",
                           authenticated=authenticated,
                           jobs=jobs,
                           children=cfg.arm_config['ARM_CHILDREN'],
                           arm_servers=arm_servers,
                           arm_path=arm_path,
                           media_path=media_path,
                           stats=stats)


@route_main.route('/systemsetup', methods=['GET', 'POST'])
@login_required
def system_info_load():
    """
    Load system initial system info
    """
    form = SystemInfoLoad()
    server_util = ServerDetails()

    if form.validate_on_submit():
        system_info = SystemInfo(name=str(form.name.data),
                                 description=str(form.description.data))
        system_info.ip_address = "127.0.0.1"
        system_info.port = 8080
        system_info.arm_type = "ui"
        system_info.cpu = str(form.cpu.data)
        system_info.cpu_usage = server_util.cpu_util
        system_info.cpu_temp = server_util.cpu_temp
        system_info.mem_total = server_util.mem_total
        system_info.mem_available = server_util.memory_free
        system_info.mem_used = server_util.memory_used
        system_info.mem_percent = server_util.memory_percent

        db.session.add(system_info)
        db.session.commit()

        current_app.logger.debug("*******SystemInfo*******")
        current_app.logger.debug(system_info.list_params())
        current_app.logger.debug("************************")

        return redirect("/index")

    return render_template("systemsetup.html",
                           form=form,
                           server_util=server_util)
