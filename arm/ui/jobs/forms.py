"""
ARM Forms Functions for:
    Jobs

Forms
    - TitleSearchForm
    - ChangeParamsForm
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, IntegerField, FieldList, \
    HiddenField, Form, FormField
from wtforms.validators import DataRequired


class TitleSearchForm(FlaskForm):
    """
    A form for Job Title Search.

    This form is used to search for job titles

    Fields:
       title (StringField): The Title of the movie or series.
       year (StringField): The Year of the movie or series.
       submit (SubmitField): A button to submit the form.

    Methods:
       validate_on_submit: Validates the form's data and checks if the form was submitted.

    Usage:
       This form is utilized on the following pages:
        - /titlesearch
        - /customTitle
        - /list_titles

    Note:
       Nil
    """
    title = StringField('Title', validators=[DataRequired()])
    year = StringField('Year')
    submit = SubmitField('Submit')


class ChangeParamsForm(FlaskForm):
    """
    A form for Change Parameters of a Job.

    This form is used to update or modify a Job's parameters.

    Fields:
       RIPMETHOD (StringField): The Rip Method of the Job.
       DISCTYPE (StringField): The Disc Type of the Job.
       MAINFEATURE (StringField): The Title of the movie or series.
       MINLENGTH (IntegerField): The minimum length of a job title.
       MAXLENGTH (IntegerField): The maximum length of a job title.
       submit (SubmitField): A button to submit the form.

    Methods:
       validate_on_submit: Validates the form's data and checks if the form was submitted.

    Usage:
       This form is utilized on the following pages:
        - /changeparams

    Note:
       Nil
    """
    RIPMETHOD = SelectField('Rip Method: ', choices=[('mkv', 'mkv'), ('backup', 'backup')])
    DISCTYPE = SelectField('Disc Type: ', choices=[('dvd', 'DVD'), ('bluray', 'Blu-ray'),
                                                   ('music', 'Music'), ('data', 'Data')])
    # "music", "dvd", "bluray" and "data"
    MAINFEATURE = BooleanField('Main Feature: ')
    MINLENGTH = IntegerField('Minimum Length: ')
    MAXLENGTH = IntegerField('Maximum Length: ')
    submit = SubmitField('Submit')


class TrackForm(Form):
    """
    Represents an individual track with an ID and a checkbox status.

    Fields:
        track_ref (HiddenField): Stores the track's unique identifier, hidden in the form.
        checkbox (BooleanField): Represents a checkbox to mark the track as selected or unselected.

    Validators:
        None

    Usage:
        - /jobdetail
    """
    track_ref = HiddenField('ID')
    checkbox = BooleanField('Checkbox')


class TrackFormDynamic(FlaskForm):
    """
    A dynamic form for managing a list of tracks in a job.

    This form is used to dynamically generate fields for each track associated
    with a job. Each track is represented by a `TrackForm` with a unique ID and
    a checkbox for user interaction.

    Attributes:
        track_ref (FieldList): A dynamic list of `TrackForm` instances, one for each track.
            - Each entry contains a hidden `track_ref` field for the ID and a `checkbox` field
              for selection.
        min_entries (int): Ensures at least one entry is present in the `FieldList`.

    Usage:
        -`/jobdetail`
    """
    track_ref = FieldList(FormField(TrackForm), min_entries=1)
