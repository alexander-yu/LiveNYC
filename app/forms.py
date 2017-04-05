from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired(),
        Length(max=20)
    ])
    password = PasswordField('password', validators=[
        InputRequired(), Length(min=8, max=20),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('confirm password')
    email = StringField('email', validators=[Email()])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired(),
        Length(max=20)
    ])
    password = PasswordField('password', validators=[
        InputRequired(), Length(min=8, max=20)
    ])
