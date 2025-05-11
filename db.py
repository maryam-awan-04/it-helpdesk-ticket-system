from datetime import date

from app import bcrypt, create_app, db
from app.models import Ticket, User

app = create_app()
app.app_context().push()

# Create all tables
db.create_all()

# Clear old data (optional, for clean setup each time)
Ticket.query.delete()
User.query.delete()
db.session.commit()

hashed_password = bcrypt.generate_password_hash("password").decode("utf-8")

user1 = User(
    firstname="Alice",
    surname="Smith",
    email="alice@gmail.com",
    password=hashed_password,
    role="Admin",
)
user2 = User(
    firstname="Bob",
    surname="Johnson",
    email="bob@gmail.com",
    password=hashed_password,
    role="User",
)
user3 = User(
    firstname="Charlie",
    surname="Brown",
    email="charlie@gmail.com",
    password=hashed_password,
    role="Admin",
)

db.session.add_all([user1, user2, user3])
db.session.commit()

ticket1 = Ticket(
    request_type="Hardware Issue",
    date_opened=date.today(),
    title="Laptop not turning on",
    description="My laptop stopped working after a Windows update.",
    status="Open",
    creator=user2.id,
)

ticket2 = Ticket(
    request_type="Access Request",
    date_opened=date.today(),
    title="Request access to Trello",
    description="Need Trello access for project tracking.",
    status="In Progress",
    assigned_to=user3.id,
    creator=user2.id,
)

ticket3 = Ticket(
    request_type="Network Issue",
    date_opened=date.today(),
    title="VPN not connecting",
    description="Cannot connect to VPN from home.",
    status="Open",
    creator=user2.id,
)

db.session.add_all([ticket1, ticket2, ticket3])
db.session.commit()

print("Test data added successfully.")
