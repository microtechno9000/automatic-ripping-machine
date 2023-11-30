"""
ARM route blueprint for sessions pages
Covers
- sessions [GET]
- sessions/edit [GET]
- sessions/update [POST]
"""

from flask_login import login_required
from flask import render_template, request, redirect

from arm.ui import app, db
from arm.ui.sessions import route_sessions
from arm.models.sessions import Sessions
from arm.models.session_settings import SessionSettings
from arm.models.session_types import SessionTypes
from arm.models.system_drives import SystemDrives
from .forms import SessionStatusForm
from .forms import SessionEditForm

"""
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


@route_sessions.route('/session')
@login_required
def sessions():
    """
    Page - Sessions
    Method - GET
    Overview - Session current state, help and link to edit pages for sessions
    """
    # Return the current session data
    db_session_types = SessionTypes.query.all()
    db_sessions = Sessions.query.all()
    # Return the current list of system drives available to ARM
    db_system_drives = SystemDrives.query.all()

    form = SessionStatusForm()

    return render_template('sessions.html',
                           db_session_types=db_session_types,
                           db_sessions=db_sessions,
                           db_system_drives=db_system_drives,
                           form=form)


@route_sessions.route('/session/edit/<session_id>', methods=['GET', 'POST'])
@login_required
def session_edit(session_id):
    """
    Page - Sessions
    Method - GET, POST
    Overview - Session editor
    """
    db_session = Sessions.query.filter_by(id=session_id).first()
    session_types = SessionTypes.query.all()

    # load data into the form
    form = SessionEditForm(request.values, obj=db_session)
    form.session_type.choices = [(record_type.id, record_type.name) for record_type in session_types]

    if form.validate_on_submit():
        app.logger.debug(f"Updating: [{form.name.data}] [{form.description.data}] [{form.session_type.data}]")
        db_session.name = form.name.data
        db_session.description = form.description.data
        db_session.type_id = form.session_type.data
        db.session.commit()
        return redirect('/session')
    else:
        app.logger.debug(f"Setting default to: {db_session.type_id}")
        form.session_type.data = db_session.type_id
        app.logger.debug(form.session_type.default)

    return render_template('session_edit.html',
                           db_session=db_session, session_types=session_types,
                           form=form)


@route_sessions.route('/session/add', methods=['GET', 'POST'])
@login_required
def session_add():
    """
    Page - Session Add
    Method - GET, POST
    Overview - Add a new Session
    """
    session_types = SessionTypes.query.all()

    # load data into the form
    form = SessionEditForm()
    form.session_type.choices = [(record_type.id, record_type.name) for record_type in session_types]

    if form.validate_on_submit():
        new_session = Sessions()
        app.logger.debug(f"Adding: [{form.name.data}] [{form.description.data}] [{form.session_type.data}]")
        new_session.name = form.name.data
        new_session.description = form.description.data
        new_session.type_id = form.session_type.data
        new_session.valid = False
        new_session.drive_id = None
        new_session.settings_id = form.session_type.data
        db.session.add(new_session)
        db.session.commit()
        return redirect('/session')
    else:
        return render_template('session_edit.html',
                               session_types=session_types,
                               form=form)


@route_sessions.route('/session/update', methods=['POST'])
@login_required
def session_update_status():
    """
    Page - Session Update
    Method - POST
    Overview - Take user updates from Session Edit tab for active and drive changes
    """
    form = SessionStatusForm()
    status = False
    clear = False
    response = "data value passed not valid"

    if form.validate():
        data = request.get_json()
        app.logger.debug(f"Session Status update: {data}")

        # Get the row ID from json, load value from database
        [name, row_id] = data['id'].split('_')
        db_session = Sessions.query.filter_by(id=int(row_id)).first()
        app.logger.debug(f"Session name: {name} row: {row_id} value: {data['value']}")

        if name == 'valid':
            db_session.valid = data['value']
            response = f"Updated Session {row_id} status"
            status = True
            app.logger.debug(f"Session db update - id: {db_session.valid}")
            db.session.commit()

        elif name == 'drive':
            # Check another session hasn't been assigned to a drive
            if int(data['value']) == 0:
                db_session.drive_id = None
                response = f"Updated Session {row_id} clearing drive"
                status = True
                app.logger.debug("Session db update - cleared drive")
                db.session.commit()
            else:
                if Sessions.query.filter_by(drive_id=int(data['value'])).count() == 0:
                    db_session.drive_id = int(data['value'])
                    response = f"Updated Session {row_id} drive"
                    status = True
                    app.logger.debug(f"Session db update - drive_id: {db_session.drive_id}")
                    db.session.commit()
                else:
                    response = f"Unable to assign Drive to Session #{row_id}, drive already assigned"
                    clear = True

    app.logger.info("Updated session information")

    return {'success': status, 'response': response, 'clear': clear}
