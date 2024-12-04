"""
Automatic Ripping Machine - User Interface (UI) - Blueprint
    Authentication

Covers
    - login_manager.user_loader
    - login_manager.unauthorized_handler
    - login [GET, POST]
    - logout [GET]
    - update_password [GET, POST]
"""
import bcrypt
from flask import redirect, render_template, request, flash, session
from flask_login import login_required, current_user, login_user, logout_user
from flask import current_app as app

from ui import db
from models.user import User
from ui.auth import route_auth
from ui.auth.forms import SetupForm

# Page definitions
page_support_databaseupdate = "support/databaseupdate.html"
redirect_settings = "/settings"


# @app.login_manager.user_loader
def load_user(user_id):
    """
    Logged in check
    :param user_id:
    :return:
    """
    try:
        return User.query.get(int(user_id))
    except Exception:
        app.logger.debug("Error getting user")
        return None


# @app.login_manager.unauthorized_handler
def unauthorized():
    """
    User isn't authorised to view the page
    :return: Page redirect
    """
    return redirect('/login')


@route_auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page if login is enabled
    :return: redirect
    """
    global page_support_databaseupdate

    # Check the database is current
    # db_update = ui_utils.arm_db_check()
    # if not db_update["db_current"] or not db_update["db_exists"]:
    #     dbform = DBUpdate(request.form)
    #     return render_template(page_support_databaseupdate, db_update=db_update, dbform=dbform)

    # return_redirect = None
    # # if there is no user in the database
    # try:
    #     user_list = User.query.all()
    #     # If we don't raise an exception but the usr table is empty
    #     if not user_list:
    #         app.logger.debug("No admin found")
    # except Exception:
    #     flash(constants.NO_ADMIN_ACCOUNT, "danger")
    #     app.logger.debug(constants.NO_ADMIN_ACCOUNT)
    #     dbform = DBUpdate(request.form)
    #     # db_update = ui_utils.arm_db_check()
    #     return render_template(page_support_databaseupdate,
    #                            db_update=db_update,
    #                            dbform=dbform)

    # if user is logged in
    if current_user.is_authenticated:
        return_redirect = redirect('/index')

    form = SetupForm()
    if request.method == 'POST' and form.validate_on_submit():
        login_password = str(request.form['password']).strip()

        # we know there is only ever 1 admin account, so we can pull it and check against it locally
        db_user = User.query.filter_by().first()
        app.logger.debug("user= " + str(db_user))

        # user details from database
        user_name = db_user.email
        user_password = db_user.password
        app.logger.debug("user= " + str(user_name))

        if bcrypt.checkpw(login_password.encode('utf-8'), user_password.encode('utf-8')):
            login_user(db_user)
            app.logger.debug("user was logged in - redirecting")
            return_redirect = redirect('/index')
        else:
            flash("Something isn't right", "danger")

    # If nothing has gone wrong, give them the login page
    if request.method == 'GET' or return_redirect is None:
        return_redirect = render_template('login.html',
                                          form=form)

    return return_redirect


@route_auth.route("/logout")
def logout():
    """
    Log user out
    :return:
    """
    logout_user()
    flash("logged out", "success")
    return redirect('/')


@route_auth.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    """
    Update the password for the admin account
    """
    # get current user
    user = User.query.first()

    session["page_title"] = "Update Admin Password"

    # After a login for is submitted
    form = SetupForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Get the new detail from the web form
        form_username = str(request.form['username']).strip()
        form_password = str(request.form['password']).strip().encode('utf-8')
        new_password = str(request.form['newpassword']).strip().encode('utf-8')

        # Get the current details from the database
        user = User.query.filter_by(email=form_username).first()

        # Check the current password is correct, if so, update
        if bcrypt.checkpw(form_password, user.password.encode('utf-8')):
            hashed_password = bcrypt.hashpw(new_password, user.hash.encode('utf-8'))
            user.password = hashed_password
            try:
                db.session.commit()
                flash("Password successfully updated", "success")
                app.logger.info("Password successfully updated")
                return redirect("logout")
            except Exception as error:
                flash(str(error), "danger")
                app.logger.debug(f"Error in updating password: {error}")
        else:
            flash("Password couldn't be updated. Problem with old password", "danger")
            app.logger.info("Password not updated, issue with old password")

    return render_template('update_password.html', user=user.email, form=form)
