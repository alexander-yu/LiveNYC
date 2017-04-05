from functools import wraps

from flask import flash, Flask, g, redirect, render_template, session, url_for
from flask_wtf import FlaskForm
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from wtforms.fields import PasswordField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, Length

import db

from config import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
engine = create_engine(URL(**settings.DATABASE))


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


def anonymous_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        username = session.get('username')
        if username:
            return redirect(url_for('login'))
        else:
            return function(*args, **kwargs)

    return wrapper


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        username = session.get('username')
        if username:
            user = db.get_user(g.cursor, username)
            if user:
                return function(*args, **kwargs)
            else:
                flash('Session exists, but user does not exist (anymore).')
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

        return wrapper


@app.before_request
def before_request():
    try:
        g.conn = engine.connect()
        g.transaction = g.conn.begin()
        g.cursor = g.conn.connection.cursor()
    except:
        import traceback
        traceback.print_exc()
        g.conn = None


@app.after_request
def after_request(response):
    g.cursor.close()
    g.transaction.commit()
    g.conn.close()
    return response


@app.teardown_request
def teardown_request(exception):
    g.cursor.close()
    g.conn.close()

    if exception is not None:
        g.transaction.rollback()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
@anonymous_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username, password, email = form.username.data, form.password.data, \
            form.email.data
        db.add_user(g.cursor, username, password, email)
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
@anonymous_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username, password = form.username.data, form.password.data
        if db.authenticate_user(g.cursor, username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', form=form, failed=True)

    return render_template('login.html', form=form, failed=False)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        HOST, PORT = host, port
        print 'running on %s:%d' % (HOST, PORT)
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()
