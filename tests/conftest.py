"""
Configuration for the application tests.
"""

import os
import sys
from datetime import datetime

import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)


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


def assert_template_renders(client, url, expected_text):
    """
    Asserts that a GET request renders correct template.
    """
    response = client.get(url)
    assert response.status_code == 200
    assert expected_text.encode("utf-8") in response.data


def create_user(
    email="creator@example.com",
    firstname="Creator",
    surname="User",
    role="User",
    password="Pass123",
):
    from app import bcrypt, db
    from app.models import User

    user = User(
        firstname=firstname,
        surname=surname,
        email=email,
        password=bcrypt.generate_password_hash(password).decode("utf-8"),
        role=role,
    )
    db.session.add(user)
    db.session.commit()
    return user


def create_ticket(
    creator,
    title="Test Ticket",
    description="This is a test ticket.",
    status="Open",
    request_type="Access Request",
    assigned_to=None,
):
    from app import db
    from app.models import Ticket

    ticket = Ticket(
        title=title,
        description=description,
        status=status,
        request_type=request_type,
        assigned_to=assigned_to,
        creator_user=creator,
        date_opened=datetime.now().date(),
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket
