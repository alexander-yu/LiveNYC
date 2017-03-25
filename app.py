from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from flask import abort, Flask, request, render_template, g, redirect

from config import settings

app = Flask(__name__)

engine = create_engine(URL(**settings.DATABASE))


@app.before_request
def before_request():
    try:
        g.conn = engine.connect()
        g.cursor = g.conn.connection.cursor()
    except:
        import traceback
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    try:
        g.conn.close()
    except Exception:
        pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
    return redirect('/')


@app.route('/login')
def login():
    abort(401)


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
