"""
Form to handle user registration
"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Regexp,
                                ValidationError)

MESSAGES = [
    "First name must contain only letters.",
    "Last name must contain only letters.",
    "Password must be at least 8 characters long.",
    "Passwords must match.",
]


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
        choices=[("User"), ("Admin")],
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

    def validate_email(self, field):
        """
        Validate that email does not already exist in the database
        """
        from app.models import User

        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Email already registered. Please sign in.")
