"""
Form to edit user details
"""

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError

MESSAGES = [
    "First name must contain only letters.",
    "Last name must contain only letters.",
]


class UserForm(FlaskForm):
    """
    Form for user registration
    """

    id = IntegerField("User ID")
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
        choices=[("Select"), ("User"), ("Admin")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")

    def validate_role(self, field):
        """
        Validate that the role is not "Select"
        """
        if field.data == "Select":
            raise ValidationError("Please select a valid role type.")
