from functools import wraps

from flask import flash, g, redirect, session, url_for

import db


def anonymous_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        username = session.get('username')
        if username:
            return redirect(url_for('index'))
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
