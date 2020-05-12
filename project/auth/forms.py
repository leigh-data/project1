from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length

from project import db, bcrypt


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

    def validate_username(self, username):
        data = {'username': self.username.data}

        count = db.session.execute(
            "SELECT COUNT(*) FROM users WHERE username=:username", data).fetchone()[0]
        if count > 0:
            raise ValidationError("Please use a different username.")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if User.login(self.username.data, self.password.data):
            return True
        else:
            self.password.errors.append('Incorrect email or password')

    def validate(self):
        rv = FlaskForm.validate_on_submit(self)
        if not rv:
            return False

        data = {'username': self.username.data}
        password_hash = db.session.execute(
            "SELECT password FROM users WHERE username=:username", data).fetchone()[0]
        if password_hash and bcrypt.check_password_hash(password_hash, self.password.data):
            return True
        else:
            print("HAHAHAHAHHA!!!!!!")
            self.password.errors.append("Incorrect username or password")
