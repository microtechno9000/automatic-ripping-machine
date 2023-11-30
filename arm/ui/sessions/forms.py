"""
Forms used in sessions blueprint
"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class SessionStatusForm(FlaskForm):
    """
    Session Status update form
    """
    id = StringField('id', validators=[DataRequired()])
    value = StringField('value')


class SessionEditForm(FlaskForm):
    """
    Session Edit
    """
    name = StringField("Session Name", validators=[InputRequired()])
    description = StringField("Session Description", validators=[InputRequired()])
    session_type = SelectField("Select a Type", coerce=int)
    submit = SubmitField('Submit')
