from flask import Flask, render_template, request, url_for, flash, redirect, session, abort, current_app
from src.config.config import Content, RegistrationForm, NewPasswordForm
from passlib.hash import sha256_crypt
from functools import wraps
from flask_jwt_extended import JWTManager
from datetime import date
from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound
import dateutil.parser as dparser
import gc
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'MovieDatabaseApp.src.config.config.DevelopmentConfig'
)
app.config.from_object(app_settings)
CONTENT = Content()

from src.decorators import login_required, BackRedirect as back

from src.models import db, engine, Actors, Movies, Users, UserRating

from flask_restful import Api
from src.resources.movies_resources import *
from src.resources.actors_resources import *
from src.resources.users_resources import *

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

api.add_resource(ActorsList, '/api/actors')
api.add_resource(Actor, '/api/actors/<actor_id>')
api.add_resource(ActorsSearch, '/api/actors/search')
api.add_resource(MoviesList, '/api/movies')
api.add_resource(Movie, '/api/movies/<movie_id>')
api.add_resource(MoviesSearch, '/api/movies/search')
api.add_resource(UserRegistration, '/api/register')
api.add_resource(User, '/api/user')
api.add_resource(TokenRefresh, '/api/user/refresh_token')
api.add_resource(UserActions, '/api/user/action')

@app.route('/')
@back.anchor
def homepage():
	return render_template('index.html', CONTENT=CONTENT)

@app.route('/movies', defaults={'path': '', 'query_type': ''}, methods=["GET"])
@app.route('/<query_type>/<path:path>/')
@back.anchor
def index(query_type, path):
	page = int(request.args['page'])
	if query_type is '' and path is '':
		res = Movies.query.order_by(Movies.rating.desc()).paginate(page, 15)
	elif query_type == 'genre':
		genre = '%{0}%'.format(path)
		res = Movies.query.filter(Movies.genre.ilike(
			genre)).order_by(Movies.rating.desc()).paginate(page, 15)
	elif query_type == 'year':
		res = Movies.query.filter(Movies.year.ilike(
			path)).order_by(Movies.rating.desc()).paginate(page, 15)
	else:
		abort(404)
	if 'logged_in' in session:
		name = session['username']
		user = Users.query.filter_by(username = name).one()
		watchlist = user.get_watchlist()
		return render_template('movielist.html', res=res, watchlist=watchlist, CONTENT=CONTENT, genre=path, query_type=query_type)
	else:
		return render_template('movielist.html', res=res, CONTENT=CONTENT, genre=path, query_type=query_type)

@app.route('/register', methods=['GET', 'POST'])
def register_page():

    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt((str(form.password.data)))

        username_check = Users.query.filter_by(username=username).count()
        email_check = Users.query.filter_by(email=email).count()

        if username_check > 0:
            flash("That username is already taken, please choose another")
            return render_template('register-v2.html', form=form, CONTENT=CONTENT)

        elif email_check > 0:
            flash("That email is already used, please choose another")
            return render_template('register-v2.html', form=form, CONTENT=CONTENT)

        else:

            db.session.add(
                Users(
                    username=username, 
                    password=password, 
                    email=email)
            )
            db.session.commit()
            flash("Thanks for registering!")
            gc.collect()

            session['logged_in'] = True
            session['username'] = username

            # return redirect(url_for('index'))
            return back.redirect()

    return render_template("register-v2.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = ''
    try:
        if request.method == "POST":

            passwd = Users.query.filter_by(
                username=request.form['username']).one().password

            if sha256_crypt.verify(request.form['password'], passwd):
                session['logged_in'] = True
                session['username'] = request.form['username']
                whalecum = 'Welcome back {0}!'.format(request.form['username'])
                flash(whalecum)
                return redirect(url_for("index", page=1))
            else:
                error = "Invalid credentials, try again."
                flash(error)

        gc.collect()

        return render_template("login-v2.html", error=error)

    except Exception as e:
        error = "Invalid credentials, try again."
        flash(str(e))
        flash(error)
        return redirect(url_for("login_page"))

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = NewPasswordForm(request.form)
    user = Users.query.filter_by(username=session['username']).one()
    if request.method == "POST" and form.validate():
        if sha256_crypt.verify(request.form['old_password'], user.password):
            user.password = sha256_crypt.encrypt((str(form.new_password.data)))
            flash('Password changed successfully.')
            db.session.commit()
            return back.redirect()
        else:
            flash('Invalid password')
    return render_template('change_password.html', form=form)

@app.route('/<path:path>/id/<object_id>')
@back.anchor
def info(path, object_id):
	if path == 'movies':
		res = Movies.query.filter_by(id=object_id).one()
		actors = res.actors
		if 'logged_in' in session:
			name = session['username']
			user = Users.query.filter_by(username = name).one()
			watchlist = user.get_watchlist()
			if res not in watchlist:
				btn = 'Add to Watchlist'
			else:
				btn = 'Remove from Watchlist'		
		else:
			btn = 'Add to Watchlist'
		return render_template('movies_info.html', res=res, CONTENT=CONTENT, actors=actors, btn=btn)
	elif path == 'actors':
		res = Actors.query.filter_by(id=object_id).one()
		movies = res.movies
		return render_template('actors_info.html', res=res, movies=movies, CONTENT=CONTENT)
	else:
		abort(404)

@app.route('/actors/popular/')
@back.anchor
def popular_celebs():
	res = db.session.query(Actors).order_by(Actors.popularity.desc()).limit(50)
	return render_template("popular_celebs.html", res=res, CONTENT=CONTENT)

@app.route('/actors/born_today/')
@back.anchor
def born_today():
    today = date.today()
    day = '%{}-{}'.format(today.month, today.day)
    def age(date_str):
        today = date.today()
        birthday = dparser.parse(date_str)
        return today.year - birthday.year - int((today.month, today.day) < (birthday.month, birthday.day))
    res = Actors.query.filter(Actors.birthday.ilike(day), Actors.deathday == '')
    return render_template("born_today.html", res=res, CONTENT=CONTENT, age=age)

@app.route('/search_result/', methods = ['POST'])
@back.anchor
def search():

    string = request.form['search']
    search_str = '%{0}%'.format(string)

    mov_res = Movies.query.filter(Movies.title.ilike(search_str))
    act_res = Actors.query.filter(Actors.name.ilike(search_str))

    return render_template('search_results-v2.html', search_str = string, mov_res = mov_res, mov_count = mov_res.count(), \
                                                act_res = act_res, act_count = act_res.count(), CONTENT = CONTENT)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('login_page'))

@app.route('/modify_watchlist')
@login_required
def modify_watchlist():
    mid = request.args.get('movieid', 0, type=str)
    movie = Movies.query.filter_by(id = mid).one()

    name = session['username']
    user = Users.query.filter_by(username = name).one()

    watchlist = user.get_watchlist()

    if movie not in watchlist:
        user.movies.append(movie)
        db.session.commit()
    else:
        user.movies.remove(movie)
        db.session.commit()

    gc.collect()

@app.route('/watchlist/', defaults = {'name' : ''})
@app.route('/watchlist/<name>')
@login_required
def watchlist(name):

	user = Users.query.filter_by(username = name).one()
	watchlist = user.get_watchlist()

	return render_template('watchlist-v2.html', watchlist = watchlist, CONTENT = CONTENT, name = name)

@app.route('/rated_movies/', defaults = {'name' : ''})
@app.route('/rated_movies/<name>')
@login_required
def rated_movies(name):

    user = Users.query.filter_by(username = name).one()
    rated = user.rated_movies

    return render_template('rated_movies.html', rated = rated, CONTENT = CONTENT, name = name)

if __name__ == "__main__":
    app.run()
