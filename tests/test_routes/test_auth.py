from app import bcrypt, db
from app.models import User


def assert_template_renders(client, url, expected_text):
    """
    Asserts that a GET request renders correct template.
    """
    response = client.get(url)
    assert response.status_code == 200
    for text in expected_text:
        assert text.encode("utf-8") in response.data


def test_login_get(client):
    """
    Tests that the login page renders correctly.
    """
    expected_text = ["Sign in", "Email", "Password"]
    assert_template_renders(client, "/auth/login", expected_text)


def test_register_get(client):
    """
    Tests that the registration page renders correctly.
    """
    expected_text = ["Register", "First Name", "Surname"]
    assert_template_renders(client, "/auth/register", expected_text)


def test_login_sets_current_user(client, test_app):
    """
    Tests that a successful login sets the current user in the session.
    """
    with test_app.app_context():
        password = "User123!"
        hashed_password = bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )
        test_user = User(
            firstname="Test",
            surname="Login",
            email="loginuser@example.com",
            password=hashed_password,
            role="User",
        )
        db.session.add(test_user)
        db.session.commit()
        test_user_id = test_user.id

    response = client.post(
        "/auth/login",
        data={"email": "loginuser@example.com", "password": password},
        follow_redirects=True,
    )
    assert response.status_code == 200

    with client.session_transaction() as session:
        assert "_user_id" in session
        assert session["_user_id"] == str(test_user_id)


def test_register_post_creates_user(client, test_app):
    """
    Tests that a successful registration creates a new user in the database.
    """
    with test_app.app_context():
        new_email = "newuser@example.com"
        registration_data = {
            "firstname": "Test",
            "surname": "User",
            "email": new_email,
            "role": "User",
            "password": "SecurePass123",
            "confirm_password": "SecurePass123",
        }

        response = client.post(
            "/auth/register", data=registration_data, follow_redirects=True
        )
        assert response.status_code == 200

        created_user = User.query.filter_by(email=new_email).first()
        assert created_user is not None
        assert created_user.firstname == "Test"
        assert created_user.role == "User"


def test_register_duplicate_email(client, test_app):
    """
    Tests that registering with an existing email prevents user creation.
    """
    with test_app.app_context():
        admin = User(
            firstname="Alice",
            surname="Smith",
            email="alice@example.com",
            role="Admin",
            password=bcrypt.generate_password_hash("AdminPass123").decode(
                "utf-8"
            ),
        )
        db.session.add(admin)
        db.session.commit()
        initial_user_count = User.query.count()

        duplicate_registration_data = {
            "firstname": "Fake",
            "surname": "Duplicate",
            "email": admin.email,
            "password": "AnotherPass123",
            "confirm": "AnotherPass123",
            "role": "User",
        }

        response = client.post(
            "/auth/register",
            data=duplicate_registration_data,
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert "already registered" in response.data.decode().lower()
        assert User.query.count() == initial_user_count


def test_logout(client):
    """
    Tests that the logout route redirects to the homepage.
    """
    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
