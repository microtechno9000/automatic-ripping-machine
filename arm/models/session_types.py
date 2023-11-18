"""
Model for the Sessions type table
"""
from arm.ui import db


class SessionTypes(db.Model):
    __tablename__ = "session_types"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    name = db.Column(db.String)
    description = db.Column(db.String)

    def __init__(self):
        # Nothing to configure or register on creation
        pass

    def __repr__(self):
        return self.id
