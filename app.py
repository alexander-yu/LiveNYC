from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from flask import Flask, g, redirect, render_template, url_for
from flask_login import current_user, LoginManager, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, Length

import db

from config import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
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


class User:
    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email

    def is_authenticated(self):
        return db.authenticate_user(g.cursor, self)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


@login_manager.user_loader
def load_user(username):
    data = db.get_user(g.cursor, username)
    if data is None:
        return None
    else:
        return User(**data)


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
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.add_user(g.cursor, user)
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        if user.is_authenticated() and login_user(user):
            return redirect(url_for('index'))
        else:
            return render_template('login.html', form=form, failed=True)

    return render_template('login.html', form=form, failed=False)


@app.route('/logout')
def logout():
    logout_user()
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
