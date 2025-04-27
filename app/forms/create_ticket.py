"""
Form to handle ticket creation
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class CreateTicket(FlaskForm):
    """
    Form for ticket creation
    """

    request_type = SelectField(
        "Request Type",
        choices=[
            ("Select"),
            ("Access Request"),
            ("Hardware Issue"),
            ("Software Issue"),
            ("Network Issue"),
            ("Security Incident"),
            ("Service Request"),
            ("Onboarding Request"),
            ("Offboarding Request"),
            ("Other"),
        ],
        validators=[DataRequired()],
    )
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Submit Details")
    create_ticket = SubmitField("Create Ticket")

    def validate_request_type(self, field):
        """
        Validate that the request type is not "Select"
        """
        if field.data == "Select":
            raise ValidationError("Please select a valid request type.")

    def validate_fields(self):
        """
        Validate that the title and description fields are not empty
        """
        if not self.title.data or not self.description.data:
            raise ValidationError("Title and description cannot be empty.")
