from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FeedbackForm(FlaskForm):
    id = StringField("Ticket ID", validators=[DataRequired()])
    rating = RadioField(
        "Rating",
        choices=[(str(i), str(i)) for i in range(1, 6)],
        validators=[
            DataRequired(),
            NumberRange(
                min=1, max=5, message="Rating must be between 1 and 5"
            ),
        ],
        coerce=int,
    )
    submit = SubmitField("Submit Feedback")
