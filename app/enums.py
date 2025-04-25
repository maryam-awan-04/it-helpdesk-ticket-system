from enum import Enum


class Role(Enum):
    ADMIN = "Admin"
    USER = "User"


class Status(Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    ON_HOLD = "On Hold"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class Department(Enum):
    PO = "Product and Operations"
    GLCE = "Gas and Low Carbon Energy"
    CP = "Customer and Products"
    STS = "Supply, Trading and Shipping"
    TECHNOLOGY = "Technology"
    STRATEGY = "Strategy"
    SUSTAINABILITY = "Sustainability"
    FINANCE = "Finance"
    LEGAL = "Legal"
    PC = "People & Culture"
