"""
Model for the Sessions type table
"""
from arm.ui import db


class SessionSettings(db.Model):
    __tablename__ = "session_settings"

    id = db.Column(db.Integer, primary_key=True)
    setting_01_id = db.Column(db.String)
    setting_01_value = db.Column(db.String)
    setting_02_id = db.Column(db.String)
    setting_02_value = db.Column(db.String)
    setting_03_id = db.Column(db.String)
    setting_03_value = db.Column(db.String)
    setting_04_id = db.Column(db.String)
    setting_04_value = db.Column(db.String)
    setting_05_id = db.Column(db.String)
    setting_05_value = db.Column(db.String)

    def __init__(self):
        # Nothing to configure or register on creation
        pass

    def __repr__(self):
        return self.id
