"""
Form to handle user login
"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError


class LoginForm(FlaskForm):
    """
    Form for user login
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

    def validate_email(self, field):
        """
        Validate that email exists in the database
        """
        from app.models import User

        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError("Email not recognised. Please register.")
        self.user = user

    def validate_password(self, field):
        """
        Validate that the password matches the hashed password in the database
        """
        from app import bcrypt

        if not hasattr(self, "user"):
            return
        if not bcrypt.check_password_hash(self.user.password, field.data):
            raise ValidationError("Incorrect password. Please try again.")
