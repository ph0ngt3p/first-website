from flask import Flask, render_template, request, url_for, flash, redirect, session, abort
from models import db
from content_management import Content
from db_connection import dbconn
from reg_form import RegistrationForm
from passlib.hash import sha256_crypt
from functools import wraps
import gc

CONTENT = Content()

app = Flask(__name__)

POSTGRES = dbconn()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)

from models import Actors, Movies, Users


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('movie_list'))

    return wrap


def get_watchlist(name):
	user = Users.query.filter_by(username = name).one()
	return Movies.query.filter(Movies.users.any(id = user.id)).all()


@app.route('/', defaults = {'path': '', 'query_type' : ''})
@app.route('/<query_type>/<path:path>/')
def movie_list(query_type, path):
    if query_type is '' and path is '':
        res = Movies.query.all()
    elif query_type == 'genre' and path in CONTENT["Top genre"]:
        genr = '%{0}%'.format(path)
        res = Movies.query.filter(Movies.genre.ilike(genr)).order_by(Movies.rating.desc())
    elif query_type == 'year':
    	res = Movies.query.filter(Movies.year.ilike(path)).order_by(Movies.rating.desc())
    else:
        abort(404)
    return render_template('main.html', res = res, CONTENT = CONTENT, path = path, query_type = query_type)


@app.route('/register/', methods = ['GET', 'POST'])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))

            x = Users.query.filter_by(username = username).count()
            y = Users.query.filter_by(email = email).count()

            if x > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form, CONTENT = CONTENT)

            elif y > 0:
                flash("That email is already used, please choose another")
                return render_template('register.html', form=form, CONTENT = CONTENT)

            else:

                db.session.add(Users(username, password, email))
                db.session.commit()
                flash("Thanks for registering!")
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('movie_list'))

        return render_template("register.html", form=form, CONTENT = CONTENT)

    except Exception as e:
        return(str(e))

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    error = ''
    try:
        if request.method == "POST":

            passwd = Users.query.filter_by(username = request.form['username']).one().password

            if sha256_crypt.verify(request.form['password'], passwd):
                session['logged_in'] = True
                session['username'] = request.form['username']
                whalecum = 'Welcome back {0}!'.format(request.form['username'])
                flash(whalecum)

            else:
                error = "Invalid credentials, try again."
                flash(error)

        gc.collect()

        return redirect(url_for("movie_list"))

    except Exception as e:
        # flash(str(e))
        flash("Invalid credentials, try again.")
        return redirect(url_for("movie_list"))


@app.route('/<path:path>/id/<object_id>/')
def info(path, object_id):
	if path == 'movies':
		res = Movies.query.filter_by(id = object_id).one()
		actors = Actors.query.filter(Actors.movies.any(id = res.id)).all()

		if 'logged_in' in session:

			name = session['username']
			watchlist = get_watchlist(name)
			if res not in watchlist:
				btn = 'Add to Watchlist'
			else:
				btn = 'Remove from Watchlist'

		else: 

			btn = 'Add to Watchlist'

		return render_template('movies_info.html', res = res, CONTENT = CONTENT, actors = actors, btn = btn)

	elif path == 'actors':
		res = Actors.query.filter_by(id = object_id).one()
		return render_template('actors_info.html', res = res, CONTENT = CONTENT)
	else:
		abort(404)

@app.route('/search_result/', methods = ['POST'])
def search():

    string = request.form['search']
    search_str = '%{0}%'.format(string)

    mov_res = Movies.query.filter(Movies.title.ilike(search_str))
    act_res = Actors.query.filter(Actors.name.ilike(search_str))

    return render_template('search_result.html', mov_res = mov_res, act_res = act_res, CONTENT = CONTENT)

@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('movie_list'))

@app.route('/modify_watchlist/')
@login_required
def modify_watchlist():
    mid = request.args.get('movieid', 0, type=str)
    movie = Movies.query.filter_by(id = mid).one()

    name = session['username']
    user = Users.query.filter_by(username = name).one()

    watchlist = get_watchlist(name)

    if movie not in watchlist:
        movie.users.append(user)
        db.session.commit()
    else:
        movie.users.remove(user)
        db.session.commit()

    gc.collect()

@app.route('/watchlist/', defaults = {'name' : ''})
@app.route('/watchlist/<name>/')
@login_required
def watchlist(name):

	watchlist = get_watchlist(name)

	return render_template('watchlist.html', watchlist = watchlist, CONTENT = CONTENT, name = name)

if __name__ == "__main__":
    app.run(debug = True)
