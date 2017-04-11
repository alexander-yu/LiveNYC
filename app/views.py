from datetime import datetime

from flask import abort, g, redirect, render_template, session, url_for

import db

from app import app
from .auth import authenticate
from .decorators import anonymous_required, login_required
from .forms import LoginForm, RegistrationForm, ReviewForm


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    favorites = db.get_favorites(g.conn, session['username'])
    reviews = db.get_reviews_by_user(g.conn, session['username'])
    return render_template('profile.html', favorites=favorites, reviews=reviews)


@app.route('/register', methods=['POST', 'GET'])
@anonymous_required
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username, password, email = form.username.data, form.password.data, \
            form.email.data
        db.add_user(g.conn, username, password, email)
        return redirect(url_for('login'))
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
@anonymous_required
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username, password = form.username.data, form.password.data
        if db.authenticate_user(g.conn, username, password):
            session['username'] = username
            return form.redirect()
        else:
            return render_template('login.html', form=form, failed=True)
    else:
        return render_template('login.html', form=form, failed=False)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/borough/<borough_name>')
def borough(borough_name):
    borough_info = db.get_borough_info(g.conn, borough_name)

    if borough_info is None:
        abort(404)

    def get_neighborhood_names():
        return db.get_neighborhood_names(g.conn, borough_name)

    def get_neighborhood_info(neighborhood_name):
        return db.get_neighborhood_info(g.conn, neighborhood_name)

    return render_template('borough.html',
                           borough_name=borough_name,
                           borough_info=borough_info,
                           get_neighborhood_names=get_neighborhood_names,
                           get_neighborhood_info=get_neighborhood_info)


@app.route('/neighborhood/<neighborhood_name>', methods=['POST', 'GET'])
def neighborhood(neighborhood_name):
    # TODO: Add functionality for starring/unstarring favorites
    neighborhood_info = db.get_neighborhood_info(g.conn, neighborhood_name)
    if neighborhood_info is None:
        abort(404)

    user = authenticate(g.conn, session)
    logged_in = user is not None
    form = ReviewForm()

    if form.validate_on_submit():
        content = form.content.data
        rating = form.rating.data
        time_written = datetime.now()
        review_data = {
            'content': content,
            'rating': rating,
            'time_written': time_written
        }
        username = user['username']

        db.add_review(g.conn, neighborhood_name, username, review_data)
        return redirect(url_for('neighborhood'),
                        neighborhood_name=neighborhood_name)
    else:
        borough_name = \
            db.get_borough_name_by_neighborhood(g.conn, neighborhood_name)

        def get_schools():
            return db.get_schools(g.conn, neighborhood_name)

        def get_parks():
            return db.get_parks(g.conn, neighborhood_name)

        def get_restaurants():
            return db.get_restaurants(g.conn, neighborhood_name)

        def get_reviews():
            return db.get_reviews_by_neighborhood(g.conn, neighborhood_name)

        return render_template('neighborhood.html',
                            neighborhood_name=neighborhood_name,
                            neighborhood_info=neighborhood_info,
                            borough_name=borough_name,
                            get_schools=get_schools,
                            get_parks=get_parks,
                            get_restaurants=get_restaurants,
                            get_reviews=get_reviews,
                            logged_in=logged_in,
                            form=form)
