# 🛠️ IT Support Ticketing System

A web-based IT Help Desk Ticketing System that enables users to submit and track support tickets, while allowing administrators to manage and resolve those tickets efficiently.

Access the web application [here](https://hissing-sara-maryam-awan-04-2cfa6604.koyeb.app/auth/login).


## 📖 Contents

- [Key Features](#🔑-key-features)
- [User Role Documentation](#👥-user-role-documentation)
- [Admin Role Documentation](#⚙️-admin-role-documentation)
- [Developer Guide](#🧑‍💻-developer-guide)

## 🔑 Key Features

- Role-based access control (User and Admin)
- User registration and authentication
- Submit and track IT support tickets
- Admin dashboard for ticket assignment and management
- Admin dashboard for user management
- Real-time ticket status updates
- Search and filter capabilities on tickets and users
- Clean and responsive UI

## 👥 User Role Documentation

### Log In

1. Visit the [Login Page](https://hissing-sara-maryam-awan-04-2cfa6604.koyeb.app/auth/login).
2. Enter your email and password.
3. Click **Sign in** to access your dashboard.

> If your email is not recognised, you’ll need to [register first](https://hissing-sara-maryam-awan-04-2cfa6604.koyeb.app/auth/register).

---

### Registration

1. Go to the [Registration Page](https://hissing-sara-maryam-awan-04-2cfa6604.koyeb.app/auth/register).
2. Fill in your details. Select **User** as your role.
3. Click **Register**.

A confirmation message will appear. You can now log in.

---

### Create a Ticket

1. Once logged in, you will see your dashboard.
2. Click **Create Ticket** in the navigation pane.
3. Fill in:
   - Title
   - Request Type
   - Description
4. Submit the form to create your ticket.

You can view the ticket status and updates in your dashboard.

---

### Update a Ticket

1. Once logged in, you will see your dashboard.
2. Click **Update Ticket** in the navigation pane.
3. Select a ticket to update from your open tickets.
3. You may update the following details for the selected ticket:
   - Title
   - Request Type
   - Description
4. Submit the form to update your ticket.

---

### Feedback

1. Navigate to your dashboard.
2. Once a ticket has been marked as 'Resolved' by an admin, the **Give Feedback** button will appear beside the ticket.
3. Click the button, rate satisfaction out of 5, and submit feedback.

This information will be used to understand areas for improvement and enhance user satisfaction.

## ⚙️ Admin Role Documentation

### Log In

1. Visit the [Login Page](https://hissing-sara-maryam-awan-04-2cfa6604.koyeb.app/auth/login).
2. Enter your email and password.
3. Click **Sign in** to access your dashboard.

> You must be registered as an admin.
> If your email is not recognised, you’ll need to [register first](https://hissing-sara-maryam-awan-04-2cfa6604.koyeb.app/auth/register).

---

### Registration

1. Go to the [Registration Page](https://hissing-sara-maryam-awan-04-2cfa6604.koyeb.app/auth/register).
2. Fill in your details. Select **Admin** as your role.
3. Click **Register**.

A confirmation message will appear. You can now log in.

---

### Dashboard

Once logged in, you will see your dashboard. Here, you can:

- View assigned tickets
- View unassigned open tickets
- Filter by request type or status

---

### Manage Tickets

Once logged in, you will see your dashboard. Click **Manage Tickets** in the navigation pane.

- View all tickets in the system
- Assign tickets to admins
- Update ticket status (e.g. In Progress, Resolved)
- Filter by creator, type, or status
- Delete tickets (with confirmation)

---

### Manage Users

Once logged in, you will see your dashboard. Click **Manage Users** in the navigation pane.

- View all registered users
- Filter users by role
- Search for users
- Edit user details
- Delete accounts

## 🧑‍💻 Developer Guide

### Tech Stack

- Python Flask (Backend)
- HTML/CSS (Frontend)
- Flask-Login (Authentication)
- Flask-WTF (Form Validation)
- SQLAlchemy (ORM)
- SQLite (Database)
- Pytest (Python testing)
- Jest (JavaScript testing)

### Getting Started

1. Clone the repository

```
git clone https://github.com/your-username/it-helpdesk-ticket-system.git
cd it-helpdesk-ticket-system
```

2. Use poetry to install the dependencies and manage virtual environments

```
poetry install
poetry shell
```

3. Run the application

```
python3 run.py
```

### Project Structure

```
it-helpdesk-ticket-system/
├── app/
│   ├── __init__.py           # App factory and config loading
│   ├── models.py             # SQLAlchemy models (e.g. User, Ticket)
│   ├── routes/               # Routes for the app (e.g. login/register/logout)
│   │   ├── auth.py
│   ├── templates/            # Templates for each of the main interfaces
│   │   ├── auth/
│   │   ├── admin/
│   │   ├── user/
│   │   └── base.html         # Template base layout
│   ├── static/
│   │   ├── auth.css
│   │   ├── base.css
│   │   └── logo.png
├── tests/
│   ├── test_routes/          # Python tests
│   └── test_scripts/         # JS tests
├── run.py                    # Entry point to start the Flask app
├── pyproject.toml            # Poetry dependency config
└── README.md
```
