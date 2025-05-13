"""
Models for the SQLite database
"""

from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(256), nullable=False)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(100), nullable=False)
    date_opened = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    date_resolved = db.Column(db.Date, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    assigned_to = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=True
    )
    creator = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    assigned_user = db.relationship("User", foreign_keys=[assigned_to])
    creator_user = db.relationship("User", foreign_keys=[creator])
