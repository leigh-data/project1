from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField
from wtforms.validators import Length, DataRequired

CHOICES = [(str(i), str(i)) for i in range(1, 6)]


class ReviewForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[
        DataRequired(),
        Length(min=1, max=500, message="Comment must be between 1 nad 500 characters")
    ])
    rating = RadioField('Rating', choices=CHOICES, default='5')


class DeleteReviewForm(FlaskForm):
    pass
