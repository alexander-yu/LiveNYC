from flask import g, redirect, render_template, session, url_for

import db

from app import app
from .decorators import anonymous_required
from .forms import LoginForm, RegistrationForm


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
