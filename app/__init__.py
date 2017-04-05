from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from config import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
engine = create_engine(URL(**settings.DATABASE))


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


from app import views  # noqa: E402, F401
