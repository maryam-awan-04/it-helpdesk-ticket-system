from conftest import assert_template_renders, create_ticket, create_user


def test_admin_dashboard_get(client, login_admin_user):
    """
    Tests that the admin dashboard page renders correctly.
    """
    expected_text = "<title>Admin Dashboard</title>"
    assert_template_renders(client, "/admin/dashboard", expected_text)


def test_admin_manage_tickets_get(client, login_admin_user):
    """
    Tests that the manage tickets page renders correctly.
    """
    expected_text = "<title>Manage Tickets</title>"
    assert_template_renders(client, "/admin/manage-tickets", expected_text)


def test_manage_users_get(client, login_admin_user):
    """
    Tests that the manage users page renders correctly.
    """
    expected_text = "<title>Manage Users</title>"
    assert_template_renders(client, "/admin/manage-users", expected_text)


def test_admin_manage_tickets_edit(client, test_app, login_admin_user):
    """
    Tests that the admin can edit a ticket.
    """
    with test_app.app_context():
        creator = create_user()
        ticket = create_ticket(creator)

        response = client.post(
            "/admin/manage-tickets",
            data={
                "id": ticket.id,
                "title": "Updated Test Ticket",
                "description": "This is an updated test ticket.",
                "status": "In Progress",
                "request_type": "Access Request",
                "assigned_to": login_admin_user.id,
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        updated = ticket.query.get(ticket.id)
        assert updated.title == "Updated Test Ticket"
        assert updated.description == "This is an updated test ticket."
        assert updated.status == "In Progress"
        assert updated.assigned_to == login_admin_user.id


def test_admin_manage_tickets_delete(client, test_app, login_admin_user):
    """
    Tests that the admin can delete a ticket.
    """
    with test_app.app_context():
        creator = create_user()
        ticket = create_ticket(creator)

        response = client.post(
            "/admin/manage-tickets",
            data={"delete_ticket": True, "delete_ticket_id": ticket.id},
            follow_redirects=True,
        )

        assert response.status_code == 200
        deleted_ticket = ticket.query.get(ticket.id)
        assert deleted_ticket is None


def test_admin_manage_users_edit(client, test_app, login_admin_user):
    """
    Tests that the admin can edit a user.
    """
    with test_app.app_context():
        user = create_user()

        response = client.post(
            "/admin/manage-users",
            data={
                "id": user.id,
                "firstname": "Updated",
                "surname": "User",
                "email": "creator@example.com",
                "role": "Admin",
            },
        )

        assert response.status_code == 200
        updated_user = user.query.get(user.id)
        assert updated_user.firstname == "Updated"
        assert updated_user.role == "Admin"


def test_admin_manage_users_delete(client, test_app, login_admin_user):
    """
    Tests that the admin can delete a user.
    """
    with test_app.app_context():
        user = create_user()

        response = client.post(
            "/admin/manage-users",
            data={"delete_user": True, "delete_user_id": user.id},
            follow_redirects=True,
        )

        assert response.status_code == 200
        deleted_user = user.query.get(user.id)
        assert deleted_user is None
