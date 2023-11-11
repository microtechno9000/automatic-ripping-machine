"""
Model for the Sessions table
"""
from arm.ui import db


class Sessions(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey("session_types.id"))
    valid = db.Column(db.Boolean)
    settings_id = db.Column(db.Integer, db.ForeignKey("session_settings.id"))
    # drive_id = db.Column(db.Integer, db.ForeignKey("system_drives.drive_id"))
    name = db.Column(db.String)
    description = db.Column(db.String)

    # Foreign key relationship
    type = db.relationship("SessionTypes", backref="Record",
                           foreign_keys=[type_id])
    settings = db.relationship("SessionSettings", backref="Record",
                               foreign_keys=[settings_id])
    # drive = db.relationship("SystemDrives", backref="Record",
    #                         foreign_keys=[drive_id])

    def __init__(self):
        # Nothing to configure or register on creation
        pass

    def __repr__(self):
        return self.id
