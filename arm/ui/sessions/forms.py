"""
Forms used in sessions blueprint
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SessionStatusForm(FlaskForm):
    """
    Session Status update form
    """
    id = StringField('id', validators=[DataRequired()])
    value = StringField('value')
