from conftest import assert_template_renders, create_user

from app.models import User


def test_login_get(client):
    """
    Tests that the login page renders correctly.
    """
    expected_text = "<title>IT Help Desk | Sign In</title>"
    assert_template_renders(client, "/auth/login", expected_text)


def test_register_get(client):
    """
    Tests that the registration page renders correctly.
    """
    expected_text = "<title>IT Help Desk | Register</title>"
    assert_template_renders(client, "/auth/register", expected_text)


def test_login_sets_current_user(client, test_app, login_admin_user):
    """
    Tests that a successful login sets the current user in the session.
    """

    response = client.post(
        "/auth/login",
        data={
            "email": "loginuser@example.com",
            "password": login_admin_user.password,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    with client.session_transaction() as session:
        assert "_user_id" in session
        assert session["_user_id"] == str(login_admin_user.id)


def test_login_invalid_email(client):
    """
    Tests that an invalid email during login returns an error message.
    """
    response = client.post(
        "/auth/login",
        data={"email": "invalid@gmail.com", "password": "WrongPass123"},
        follow_redirects=True,
    )

    expected_text = "Email not recognised. Please register."
    assert expected_text in response.data.decode()


def test_login_invalid_password(client, test_app):
    """
    Tests that an invalid password during login returns an error message.
    """
    user = create_user()

    response = client.post(
        "/auth/login",
        data={"email": user.email, "password": "WrongPass123"},
        follow_redirects=True,
    )
    print(response.data.decode())

    expected_text = "Incorrect password. Please try again."
    assert expected_text in response.data.decode()


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
        user = create_user()
        initial_user_count = User.query.count()

        duplicate_registration_data = {
            "firstname": "Fake",
            "surname": "Duplicate",
            "email": user.email,
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
        expected_text = "Email already registered. Please sign in."
        assert expected_text in response.data.decode()
        assert User.query.count() == initial_user_count


def test_register_invalid_role(client, test_app):
    """
    Tests that an invalid role during registration returns an error message.
    """
    with test_app.app_context():
        invalid_registration_data = {
            "firstname": "Test",
            "surname": "User",
            "email": "test@gmail.com",
            "role": "Select",
            "password": "SecurePass123",
            "confirm_password": "SecurePass123",
        }

        response = client.post(
            "/auth/register",
            data=invalid_registration_data,
            follow_redirects=True,
        )

        assert response.status_code == 200
        expected_text = "Please select a valid role."
        assert expected_text in response.data.decode()


def test_logout(client):
    """
    Tests that the logout route redirects to the login page.
    """
    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert_template_renders(
        client, "/auth/login", "<title>IT Help Desk | Sign In</title>"
    )
