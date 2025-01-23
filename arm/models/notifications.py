import datetime

from models.arm_models import ARMModel
from models.db_setup import db


class Notifications(ARMModel):
    """
    ARM Database Model - Notifications

    Each notification has an ID, a boolean indicating if it has been seen,
    the time when it was triggered, the time when it was dismissed (if dismissed),
    a title, a message, a boolean indicating if it has been cleared,
    the time when it was cleared, and a difference time property (None by default).

    Database Table:
        notifications

    Attributes:
        id (int): The unique identifier for the notification.
        seen (bool): Indicates if the notification has been seen.
        trigger_time (datetime): The time when the notification was triggered.
        dismiss_time (datetime): The time when the notification was dismissed.
        title (str): The title of the notification.
        message (str): The content/message of the notification.
        cleared (bool): Indicates if the notification has been cleared.
        cleared_time (datetime): The time when the notification was cleared.
        diff_time (None): Difference time property, initialized as None.

    Relationships:
        None
    """
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    seen = db.Column(db.Boolean)
    trigger_time = db.Column(db.DateTime)
    dismiss_time = db.Column(db.DateTime)
    title = db.Column(db.String(256))
    message = db.Column(db.Text)
    diff_time = None
    cleared = db.Column(db.Boolean, default=False, nullable=False)
    cleared_time = db.Column(db.DateTime)

    def __init__(self, title: str = None, message: str = None):
        self.seen = False
        self.trigger_time = datetime.datetime.now()
        self.title = title
        self.message = message
