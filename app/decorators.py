from functools import wraps

from flask import g, redirect, request, session, url_for

from .auth import authenticate


def anonymous_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user = authenticate(g.conn, session)
        if user:
            return redirect(url_for('index'))
        else:
            return function(*args, **kwargs)

    return wrapper


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user = authenticate(g.conn, session)
        if user:
            return function(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.endpoint))

    return wrapper
