# 🛠️ IT Support Ticketing System

A web-based IT Help Desk Ticketing System that enables users to submit and track support tickets, while allowing administrators to manage and resolve those tickets efficiently.


## 📖 Contents

- [Key Features](#key-features)
- [User Role Documentation](#user-role-documentation)
- [Admin Role Documentation](#admin-role-documentation)
- [Developer Guide](#developer-guide)

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

1. Visit the [Login Page](/auth/login).
2. Enter your email and password.
3. Click **Sign in** to access your dashboard.

> If your email is not recognised, you’ll need to [register first](/auth/register).

---

### Registration

1. Go to the [Registration Page](/auth/register).
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

1. Visit the [Login Page](/auth/login).
2. Enter your email and password.
3. Click **Sign in** to access your dashboard.

> You must be registered as an admin.
> If your email is not recognised, you’ll need to [register first](/auth/register).

---

### Registration

1. Go to the [Registration Page](/auth/register).
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

- Flask (Backend Framework)
- Flask-Login (Authentication)
- Flask-WTF (Form Validation)
- SQLAlchemy (ORM)
- SQLite (Database)
- Pytest (Python testing)
- Jest (JavaScript testing)
