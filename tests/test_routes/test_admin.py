from conftest import create_ticket, create_user


def test_admin_dashboard_get(client, login_admin_user):
    """
    Tests that the admin dashboard page renders with and without filters.
    """
    create_ticket(
        login_admin_user, status="Open", request_type="Access Request"
    )
    create_ticket(login_admin_user, status="Closed", request_type="Other")

    response = client.get("/admin/dashboard")
    assert "<title>Admin Dashboard</title>" in response.data.decode()

    # With filters
    response = client.get(
        "/admin/dashboard?status=Open&request_type=Access Request"
    )
    assert "<title>Admin Dashboard</title>" in response.data.decode()


def test_admin_manage_tickets_get(client, login_admin_user):
    """
    Tests that the manage tickets page with and without filters.
    """
    create_ticket(
        login_admin_user, status="Open", request_type="Access Request"
    )
    create_ticket(login_admin_user, status="Closed", request_type="Other")

    # No filters
    response = client.get("/admin/manage-tickets")
    assert "<title>Manage Tickets</title>" in response.data.decode()

    # With filters
    response = client.get(
        "/admin/manage-tickets?status=Open&request_type=Access Request"
    )
    assert "<title>Manage Tickets</title>" in response.data.decode()


def test_admin_manage_users_get(client, login_admin_user):
    """
    Tests that the manage users page renders with and without users.
    """
    create_user(email="admin@gmail.com", role="Admin")
    create_user(email="user@gmail.com", role="User")

    # No filters
    response = client.get("/admin/manage-users")
    assert "<title>Manage Users</title>" in response.data.decode()

    # With filters
    response = client.get("/admin/manage-users?role=Admin")
    assert "<title>Manage Users</title>" in response.data.decode()


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
