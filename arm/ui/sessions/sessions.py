"""
ARM route blueprint for sessions pages
Covers
- sessions [GET]
"""

import os
import platform
import importlib
from flask_login import login_required
from flask import render_template, Blueprint

import arm.ui.utils as ui_utils
from arm.ui import app, db
from arm.models import models as models
import arm.config.config as cfg
from arm.ui.forms import SettingsForm, UiSettingsForm, AbcdeForm, SystemInfoDrives
from arm.ui.settings.ServerUtil import ServerUtil

route_sessions = Blueprint('route_sessions', __name__,
                           template_folder='templates',
                           static_folder='../static')


"""
TODO:
- define workflow
- define session_settings for each of the arm data types from arm.yaml

Pages
    Create
    - sessions
        create, read, update and delete sessions
        view the current session
        view current jobs against sessions
        enable/disable listed sessions
        assign session to a drive
        assign a session to all drives
            report error when assigning to more than one drive

    - sessiontypeview
        create, read, update and delete session types
        view list of all session types
        remove current session types
        add new session types
        edit session types
        above leads to 'sessiontypeditor'

    - sessiontypeditor
        detailed editor for the session_types

    Update
    - settings
        update drives to include the current session, with link to the session page
    - jobs
        update jobs to reference the current session, with link to the session page
    - index
        update current job detail to include session ID

Plan/workflow
- new session is created and assigned to a drive, or all drives. system_drives records which session is against each drive
- multiple sessions can be valid and in operational, although only one session can be valid per drive
- creating a new session links the session types to the drive(s) to run the session
- session types, come predefined with some values, although user can edit and modify
- data types are defined and not user editable, these should aign with existing arm functionality

database
ADDED
:system_drives
    session         [foreign_key:sessions->id]

NEW
:sessions
    id              [primary_key]
    name            [varchar]
    description     [varchar]
    session_type    [foreign_key:session_type->id]
    valid           [boolean]
        true - will execute against 'drive'
        false - normal ARM operation

    ::data
    id  name           description          session_type    valid
    1   USER_DEF_1     USER_DESCRIPTION_1   1               1
    2   USER_DEF_1     USER_DESCRIPTION_1   2               0

:session_type
    id              [primary_key]
    data_type       [foreign_key:data_type->id]
    name            [varchar]
    description     [varchar]
    type_settings   [foreign_key:session_settings->id]
        override ARM default settings for the media type and use here

    ::data
    id  data_type   name                description
    1   1           Movie - DVD         ARM session to rip DVD movies
    2   2           Movie - Blueray     ARM sessionto rip Bluray movies
    3   1           TV - DVD            ARM session to rip DVD TV Series
    4   2           TV - Blueray        ARM session to rip Bluray TV Series
    5   3           Music - MP3         ARM session to rip music as mp3
    6   3           Music - flac        ARM session to rip music as flac
    6   4           Data                ARM session to rip data disk
    7   1           HomeMovie - DVD     ARM session to rip dvd contents but with no title lookup
    8   2           HomeMovie - Bluray  ARM session to rip dvd contents but with no title lookup
    7   5           ISO                 ARM session to create ISO

:session_settings
    id              [primary_key]
    setting_01      [varchar]
    setting_02      [varchar]
    setting_03      [varchar]
    setting_04      [varchar]
    setting_05      [varchar]
    setting_06      [varchar]
    setting_07      [varchar]
    setting_08      [varchar]
    setting_09      [varchar]
    setting_10      [varchar]

:data_type
    id              [primary_key]
    type            [varchar]
    name            [varchar]
    description     [varchar]

    ::data
    id  type        name            description
    1   dvd         DVD             ARM will rip new media as a movie
    2   blueray     Bluray          ARM will rip new media as a blueray movie
    3   music       Music           ARM will rip new media as a music
    4   data        Data            ARM will rip new media as a data disk (copy contents)
    5   iso         ISO             ARM will rip new media as an ISO image of the disk

"""


@route_sessions.route('/sessions')
@login_required
def settings():
    """
    Page - settings
    Method - GET
    Overview - allows the user to update the all configs of A.R.M without
    needing to open a text editor
    """


    return render_template('sessions.html')
