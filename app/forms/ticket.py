"""
Form to handle ticket creation or update
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class CreateTicketForm(FlaskForm):
    """
    Form for ticket creation or update
    """

    class Meta:
        csrf = False

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


class UpdateTicketForm(FlaskForm):
    """
    Form for ticket update
    """

    class Meta:
        csrf = False

    id = StringField("Ticket ID", validators=[DataRequired()])
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
    status = SelectField(
        "Status",
        choices=[
            ("Select"),
            ("Open"),
            ("In Progress"),
            ("On Hold"),
            ("Resolved"),
            ("Closed"),
        ],
        validators=[DataRequired()],
    )
    assigned_to = SelectField(
        "Assigned To", choices=[("", "Select an admin")], coerce=str
    )
    submit = SubmitField("Update Ticket")

    def validate_assigned_to(self, field):
        """
        Validate that the assigned to field is compulsory if status != "Open"
        """
        if self.status.data != "Open" and not field.data:
            raise ValidationError(
                "Assigned to field is required when status is not 'Open'."
            )
