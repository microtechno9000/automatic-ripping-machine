"""
ARM route blueprint for sessions pages
Covers
- sessions [GET]
"""

from flask_login import login_required
from flask import render_template

from arm.ui.sessions import route_sessions
from arm.models import Sessions
from arm.models import SessionSettings
from arm.models import SessionTypes

import arm.ui.utils as ui_utils
from arm.ui import app, db
from arm.models import models as models
import arm.config.config as cfg
from arm.ui.forms import SettingsForm, UiSettingsForm, AbcdeForm, SystemInfoDrives
from arm.ui.settings.ServerUtil import ServerUtil


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

Plan
    - new session is created and assigned to a drive, or all drives. system_drives records which session is against \
    each drive
    - multiple sessions can be valid and in operational, although only one session can be valid per drive
    - creating a new session links the session types to the drive(s) to run the session
    - session types, come predefined with some values, although user can edit and modify
    - data types are defined and not user editable, these should aign with existing arm functionality

Workflow
    - Ripper
        - Get drive ID (srX)
        - check db for session against drive
        - call the associated function for the session
    - UI

database
:data_type
    data type holds the configuration detailing the various ripping methods
    
    ::structure
    id              [primary_key]
    type            [varchar]
    name            [varchar]
    description     [varchar]

    ::data
    id  type        name            description
    1   dvd         DVD             ARM will rip new media using handbrake (for DVDs)
    2   blueray     Bluray          ARM will rip new media using makemkv (for Blurays)
    3   music       Music           ARM will rip new media using abcde (for Music)
    4   data        Data            ARM will rip new media by copying contents
    5   iso         ISO             ARM will rip new media using dd or ddrescue

:sessions
    session type holds the user configured session against the data type
    
    ::structure
    id              [primary_key]
    data_type       [foreign_key:data_type->id]
    valid           [boolean]
        true - will execute against 'drive'
        false - normal ARM operation
    settings        [foreign_key:session_settings->id]
    name            [varchar]
    description     [varchar]
    type_settings   [foreign_key:session_settings->id]
        override ARM default settings for the media type and use here

    ::data
    id  data_type   valid   settings   name                description
    01   1           T/F     [x]        Movie - DVD         ARM session to rip DVD movies
    02   2           T/F     [x]        Movie - Blueray     ARM sessionto rip Bluray movies
    03   1           T/F     [x]        TV - DVD            ARM session to rip DVD TV Series
    04   2           T/F     [x]        TV - Blueray        ARM session to rip Bluray TV Series
    05   3           T/F     [x]        Music - MP3         ARM session to rip music as mp3
    06   3           T/F     [x]        Music - flac        ARM session to rip music as flac
    07   4           T/F     [x]        Data                ARM session to rip data disk
    08   1           T/F     [x]        HomeMovie - DVD     ARM session to rip dvd contents but with no title lookup
    09   2           T/F     [x]        HomeMovie - Bluray  ARM session to rip dvd contents but with no title lookup
    10   5           T/F     [x]        ISO                 ARM session to create ISO using dd
    11   5           T/F     [x]        ISO                 ARM session to create ISO using ddrescue

:session_settings
    table to hold the configuration data foe each of the sessions
    TODO: define the settings config
    
    ::structure
    id                  [primary_key]
    setting_01_id       [string]
        holds the name of the setting to configure
    setting_01_value    [string]
        holds the value of the setting
    
    ::data
    id              [primary_key]
    setting_01      [varchar]
    setting_02      [varchar]
    ...
    setting_n       [varchar]
"""


@route_sessions.route('/sessions')
@login_required
def sessions():
    """
    Page - Sessions
    Method - GET
    Overview - allows the user to update the session configuration
    """

    db_session_types = SessionTypes.SessionTypes.query.all()
    db_sessions = Sessions.Sessions.query.all()

    return render_template('sessions.html',
                           db_session_types=db_session_types,
                           db_sessions=db_sessions)
