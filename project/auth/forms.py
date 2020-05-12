from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length

from project import db


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=5, max=25, message="Username must be between 5 and 25 characaters")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=25, message="Password must be between 8 and 25 characters")
    ])
    password2 = PasswordField('Confirm Password',
                              validators=[
                                  DataRequired(), EqualTo('password')
                              ])
