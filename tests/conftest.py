"""
Configuration for the application tests.
"""

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

import pytest


@pytest.fixture
def test_app():
    from app import create_app, db, models

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
            "LOGIN_DISABLED": False,
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def runner(test_app):
    return test_app.test_cli_runner()


@pytest.fixture
def login_admin_user(client, test_app):
    from app import bcrypt, db
    from app.models import User

    with test_app.app_context():
        password = "Admin123!"
        admin = User(
            firstname="Admin",
            surname="Test",
            email="admin@example.com",
            password=bcrypt.generate_password_hash(password).decode("utf-8"),
            role="Admin",
        )
        db.session.add(admin)
        db.session.commit()

        client.post(
            "/auth/login",
            data={"email": admin.email, "password": password},
            follow_redirects=True,
        )
    return admin
