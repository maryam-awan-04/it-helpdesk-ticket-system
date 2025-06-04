"""
Initialisation of the Flask application and its components
"""

import os

from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .routes import admin, auth, user

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Set the secret key
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

    # Configure database
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "../helpdesk.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(user.bp)

    # Route to login page
    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    # Create database tables
    with app.app_context():
        from . import models
        from .data import ticket_entries, user_entries

        db.drop_all()
        db.create_all()

        for new_user in user_entries():
            if not models.User.query.filter_by(email=new_user.email).first():
                db.session.add(new_user)
        db.session.commit()

        for new_ticket in ticket_entries():
            db.session.add(new_ticket)
        db.session.commit()

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User

    return User.query.get(int(user_id))
