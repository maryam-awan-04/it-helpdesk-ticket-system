from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FeedbackForm(FlaskForm):
    rating = RadioField(
        "Rating",
        choices=[(str(i), f"{i} Stars") for i in range(1, 6)],
        validators=[
            DataRequired(),
            NumberRange(min=1, max=5, message="Rating must be between 1 and 5"),
        ],
    )
    submit = SubmitField("Submit Feedback")
