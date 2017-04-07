from flask import Flask, render_template, request, url_for, flash, redirect, session, abort, current_app
from src.config.config import Content, RegistrationForm
from passlib.hash import sha256_crypt
from functools import wraps
from flask_jwt_extended import JWTManager
import gc
import os

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'MovieDatabaseApp.src.config.config.DevelopmentConfig'
)
app.config.from_object(app_settings)
CONTENT = Content()

from src.decorators import login_required, BackRedirect as back

from src.models import db, Actors, Movies, Users

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

@app.route('/', defaults={'path': '', 'query_type': ''})
@app.route('/<query_type>/<path:path>/')
@back.anchor
def index(query_type, path):
    if query_type is '' and path is '':
        res = Movies.query.all()
    elif query_type == 'genre' and path in CONTENT["Top genre"]:
        genr = '%{0}%'.format(path)
        res = Movies.query.filter(Movies.genre.ilike(
            genr)).order_by(Movies.rating.desc())
    elif query_type == 'year':
    	res = Movies.query.filter(Movies.year.ilike(
    	    path)).order_by(Movies.rating.desc())
    else:
        abort(404)
    return render_template('main.html', res=res, CONTENT=CONTENT, path=path, query_type=query_type)


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
            return render_template('register.html', form=form, CONTENT=CONTENT)

        elif email_check > 0:
            flash("That email is already used, please choose another")
            return render_template('register.html', form=form, CONTENT=CONTENT)

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

    return render_template("register.html", form=form, CONTENT=CONTENT)


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
                # return redirect(url_for("index"))
                return back.redirect()
            else:
                error = "Invalid credentials, try again."
                flash(error)

        gc.collect()

        return render_template("login.html", error=error, CONTENT=CONTENT)

    except Exception as e:
        error = "Invalid credentials, try again."
        flash(str(e))
        flash(error)
        return redirect(url_for("login_page"))


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

@app.route('/search_result/', methods = ['POST'])
def search():

    string = request.form['search']
    search_str = '%{0}%'.format(string)

    mov_res = Movies.query.filter(Movies.title.ilike(search_str))
    act_res = Actors.query.filter(Actors.name.ilike(search_str))

    return render_template('search_result.html', mov_res = mov_res, act_res = act_res, CONTENT = CONTENT)

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

	return render_template('watchlist.html', watchlist = watchlist, CONTENT = CONTENT, name = name)

if __name__ == "__main__":
    app.run()
