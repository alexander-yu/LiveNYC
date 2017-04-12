from flask import Flask, g, session
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from config import settings

import db

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
engine = create_engine(URL(**settings.DATABASE))


@app.context_processor
def inject_username():
    return {'username': session.get('username')}


@app.context_processor
def inject_borough_names():
    def get_borough_names():
        return db.get_borough_names(g.conn)

    return {'get_borough_names': get_borough_names}


@app.before_request
def before_request():
    try:
        g.conn = engine.connect()
        g.transaction = g.conn.begin()
    except:
        import traceback
        traceback.print_exc()
        g.conn = None


@app.after_request
def after_request(response):
    g.transaction.commit()
    g.conn.close()
    return response


@app.teardown_request
def teardown_request(exception):
    if g.conn is not None:
        g.conn.close()

    if exception is not None:
        g.transaction.rollback()


from app import views  # noqa: E402, F401
