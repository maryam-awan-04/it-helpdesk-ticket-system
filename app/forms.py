"""
Forms for the Flask application
e.g. login, registration
"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

MESSAGES = [
    "First name must contain only letters.",
    "Last name must contain only letters.",
    "Password must be at least 8 characters long.",
    "Passwords must match.",
]


class LoginForm(FlaskForm):
    """
    Form for user login
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class RegistrationForm(FlaskForm):
    """
    Form for user registration
    """

    firstname = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Regexp(r"^[A-Za-z]+$", message=MESSAGES[0]),
        ],
    )
    surname = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Regexp(r"^[A-Za-z]+$", message=MESSAGES[1]),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = SelectField(
        "Role",
        choices=[("User", "User"), ("Admin", "Admin")],
        validators=[DataRequired()],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message=MESSAGES[2]),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message=MESSAGES[3]),
        ],
    )
    submit = SubmitField("Register")
