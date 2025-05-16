from conftest import assert_template_renders, create_ticket, create_user


def test_user_dashboard_get(client, login_admin_user):
    """
    Tests that the user dashboard page renders correctly.
    """
    expected_text = "<title>User Dashboard</title>"
    assert_template_renders(client, "/user/dashboard", expected_text)


def test_user_create_ticket_get(client, login_admin_user):
    """
    Tests that the create ticket page renders correctly.
    """
    expected_text = "<title>Create Ticket</title>"
    assert_template_renders(client, "/user/create-ticket", expected_text)


def test_user_update_ticket_get(client, login_admin_user):
    """
    Tests that the update ticket page renders correctly.
    """
    expected_text = "<title>Update Ticket</title>"
    assert_template_renders(client, "/user/update-ticket", expected_text)


def test_user_create_ticket_post(client, test_app, login_admin_user):
    """
    Tests that a user can create a ticket.
    """
    with test_app.app_context():
        creator = create_user()
        ticket = create_ticket(creator)

        response = client.post(
            "/user/create-ticket",
            data={
                "title": "Test Ticket",
                "description": "This is a test ticket.",
                "status": "Open",
                "request_type": "Access Request",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        ticket = ticket.query.get(ticket.id)
        assert ticket is not None
        assert ticket.title == "Test Ticket"
        assert ticket.description == "This is a test ticket."


def test_user_update_ticket_post(client, test_app, login_admin_user):
    """
    Tests that a user can update a ticket.
    """
    with test_app.app_context():
        creator = login_admin_user
        ticket = create_ticket(creator)

        response = client.post(
            "/user/update-ticket",
            data={
                "ticket_id": ticket.id,
                "title": "Updated Test Ticket",
                "description": "This is an updated test ticket.",
                "request_type": "Security Incident",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        updated = ticket.query.get(ticket.id)
        assert updated.title == "Updated Test Ticket"
        assert updated.description == "This is an updated test ticket."
        assert updated.request_type == "Security Incident"


def test_user_submit_feedback_post(client, test_app, login_admin_user):
    """
    Tests that a user can submit feedback for a ticket.
    """
    with test_app.app_context():
        creator = create_user()
        ticket = create_ticket(creator)

        response = client.post(
            "/user/submit-feedback",
            data={"id": ticket.id, "rating": "3"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        updated = ticket.query.get(ticket.id)
        assert updated.feedback == "3"
