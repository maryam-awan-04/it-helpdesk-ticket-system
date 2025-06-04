"""
Functions to add entries to the database.
"""


def encrypt_password(password):
    from flask_bcrypt import Bcrypt

    bcrypt = Bcrypt()
    return bcrypt.generate_password_hash(password).decode("utf-8")


def user_entries():
    from . import models

    new_users = [
        models.User(
            firstname="John",
            surname="Smith",
            email="john.smith@gmail.com",
            password=encrypt_password("Password123!"),
            role="User",
        ),
        models.User(
            firstname="Jane",
            surname="Doe",
            email="jane.doe@gmail.com",
            password=encrypt_password("randomPassword0"),
            role="Admin",
        ),
        models.User(
            firstname="Alice",
            surname="Johnson",
            email="alice.johnson@gmail.com",
            password=encrypt_password("Pets1!"),
            role="User",
        ),
        models.User(
            firstname="Bob",
            surname="Miller",
            email="bob.miller@gmail.com",
            password=encrypt_password("schoolClass456"),
            role="Admin",
        ),
        models.User(
            firstname="Charlie",
            surname="Brown",
            email="charlie.brown@gmail.com",
            password=encrypt_password("MyPassword789!"),
            role="User",
        ),
        models.User(
            firstname="Richard",
            surname="Wilson",
            email="richard.wilson@gmail.com",
            password=encrypt_password("SecurePass123"),
            role="User",
        ),
        models.User(
            firstname="Emily",
            surname="Davis",
            email="emily.davis@gmail.com",
            password=encrypt_password("MySecurePassword!"),
            role="User",
        ),
        models.User(
            firstname="Anna",
            surname="Scott",
            email="anna.scot@gmail.com",
            password=encrypt_password("Password!1234"),
            role="Admin",
        ),
        models.User(
            firstname="Michael",
            surname="Taylor",
            email="michael.taylor@gmail.com",
            password=encrypt_password("RandomPassword321"),
            role="User",
        ),
        models.User(
            firstname="Sean",
            surname="Williams",
            email="sean.williams@gmail.com",
            password=encrypt_password("Secure123!"),
            role="User",
        ),
    ]

    return new_users


def ticket_entries():
    from datetime import date

    from . import models

    new_tickets = [
        models.Ticket(
            request_type="Access Request",
            date_opened=date(2025, 5, 1),
            title="Access to Company Resources",
            description="Requesting access to company resources for new employee.",
            status="Closed",
            date_resolved=date(2025, 5, 2),
            feedback=3,
            assigned_to=4,
            creator=1,
        ),
        models.Ticket(
            request_type="Hardware Issue",
            date_opened=date(2025, 5, 5),
            title="Laptop Not Booting",
            description="The laptop does not boot up.",
            status="In Progress",
            date_resolved=None,
            feedback=None,
            assigned_to=2,
            creator=3,
        ),
        models.Ticket(
            request_type="Hardware Issue",
            date_opened=date(2025, 5, 12),
            title="Printer Not Responding",
            description="The office printer is not responding to print commands.",
            status="Resolved",
            date_resolved=date(2025, 5, 16),
            feedback=None,
            assigned_to=2,
            creator=1,
        ),
        models.Ticket(
            request_type="Software Issue",
            date_opened=date(2025, 5, 15),
            title="Software Installation Request",
            description="Requesting installation of software on my laptop.",
            status="On Hold",
            date_resolved=None,
            feedback=None,
            assigned_to=4,
            creator=5,
        ),
        models.Ticket(
            request_type="Network Issue",
            date_opened=date(2025, 5, 16),
            title="Wi-Fi Connectivity Problem",
            description="Unable to connect to the Wi-Fi network.",
            status="Resolved",
            date_resolved=date(2025, 5, 17),
            feedback=None,
            assigned_to=10,
            creator=6,
        ),
        models.Ticket(
            request_type="Security Incident",
            date_opened=date(2025, 5, 20),
            title="Phishing Email Report",
            description="Received a suspicious email that may be a phishing attempt.",
            status="Closed",
            date_resolved=date(2025, 5, 21),
            feedback=4,
            assigned_to=8,
            creator=7,
        ),
        models.Ticket(
            request_type="Service Request",
            date_opened=date(2025, 5, 21),
            title="Request for New Monitor",
            description="Requesting a new monitor for my workstation.",
            status="Open",
            date_resolved=None,
            feedback=None,
            assigned_to=None,
            creator=9,
        ),
        models.Ticket(
            request_type="Onboarding Request",
            date_opened=date(2025, 5, 27),
            title="New Employee Onboarding",
            description="Requesting onboarding for a new employee.",
            status="In Progress",
            date_resolved=None,
            feedback=None,
            assigned_to=8,
            creator=10,
        ),
        models.Ticket(
            request_type="Offboarding Request",
            date_opened=date(2025, 6, 1),
            title="Employee Offboarding Process",
            description="Requesting offboarding for an employee leaving the company.",
            status="In Progress",
            date_resolved=None,
            feedback=None,
            assigned_to=4,
            creator=1,
        ),
        models.Ticket(
            request_type="Other",
            date_opened=date(2025, 6, 5),
            title="Other",
            description="Need assistance with relocating my desk to a new office space.",
            status="In Progress",
            date_resolved=None,
            feedback=None,
            assigned_to=8,
            creator=1,
        ),
        models.Ticket(
            request_type="Access Request",
            date_opened=date(2025, 6, 10),
            title="Access to Shared Drive",
            description="Requesting access to the shared drive for project files.",
            status="Open",
            date_resolved=None,
            feedback=None,
            assigned_to=None,
            creator=1,
        ),
    ]

    return new_tickets
