from urlparse import urlparse, urljoin

from flask import request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms.fields import HiddenField, PasswordField, RadioField
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional


SCHEMES = {'HTTP', 'HTTPS', 'http', 'https'}


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in SCHEMES and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

    return None


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired(),
        Length(max=20)
    ])
    password = PasswordField('password', validators=[
        InputRequired(), Length(min=8, max=20),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('confirm password', validators=[InputRequired()])
    email = StringField('email', validators=[Email()])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target()

    def redirect(self, fallback_endpoint='index', **kwargs):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)

        else:
            target = get_redirect_target()
            return redirect(target or url_for(fallback_endpoint, **kwargs))


class ReviewForm(FlaskForm):
    rating = RadioField('rating', choices=[
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ], coerce=int, validators=[InputRequired()])
    content = TextAreaField('review', validators=[
        Length(max=1000), Optional()
    ])
