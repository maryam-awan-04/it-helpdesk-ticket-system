from datetime import datetime, timezone

from . import db
from .enums import Department, Role, Status


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)

    tickets = db.relationship("Ticket", backref="creator", lazy=True)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(Status), default=Status.NEW, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    department = db.Column(db.Enum(Department), nullable=True)
