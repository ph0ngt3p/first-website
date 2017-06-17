# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table, text, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from MovieDatabaseApp import app

db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
metadata = db.metadata

t_actors_by_movies = db.Table(
    'actors_by_movies', metadata,
    db.Column('movie_id', ForeignKey(u'movies_info.id'), primary_key=True, nullable=False),
    db.Column('actor_id', ForeignKey(u'actors_info.id'), primary_key=True, nullable=False)
)

class CRUD():   
 
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()   
 
    def update(self):
        return db.session.commit()
 
    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

class Actors(db.Model, CRUD):
    __tablename__ = 'actors_info'

    id = db.Column(Integer, primary_key=True, server_default=text("nextval('actors_info_id_seq'::regclass)"))
    aka = db.Column(String(250), server_default=text("NULL::character varying"))
    biography = db.Column(String(5000), server_default=text("NULL::character varying"))
    birthday = db.Column(String(128), server_default=text("NULL::character varying"))
    deathday = db.Column(String(128), server_default=text("NULL::character varying"))
    gender = db.Column(String(5), server_default=text("NULL::character varying"))
    homepage = db.Column(String(250), server_default=text("NULL::character varying"))
    tmdbid = db.Column(Integer, nullable=False, unique=True)
    imdbid = db.Column(String(128), server_default=text("NULL::character varying"))
    name = db.Column(String(250), server_default=text("NULL::character varying"))
    place_of_birth = db.Column(String(250), server_default=text("NULL::character varying"))
    popularity = db.Column(Float(53))
    profile_pic = db.Column(String(500), server_default=text("NULL::character varying"))

    movies = db.relationship(u'Movies', secondary='actors_by_movies')

    def __init__(self, *args, **kwargs):
        super(Actors, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Actors %r>' % self.name


class Movies(db.Model, CRUD):
	__tablename__ = 'movies_info'

	id = db.Column(Integer, primary_key=True, server_default=text("nextval('movies_info_id_seq'::regclass)"))
	title = db.Column(String(128), server_default=text("NULL::character varying"))
	year = db.Column(String(128), server_default=text("NULL::character varying"))
	rated = db.Column(String(128), server_default=text("NULL::character varying"))
	released = db.Column(String(128), server_default=text("NULL::character varying"))
	runtime = db.Column(String(128), server_default=text("NULL::character varying"))
	genre = db.Column(String(128), server_default=text("NULL::character varying"))
	director = db.Column(String(1000), server_default=text("NULL::character varying"))
	writer = db.Column(String(1000), server_default=text("NULL::character varying"))
	casts = db.Column(String(500), server_default=text("NULL::character varying"))
	plot = db.Column(String(5000), server_default=text("NULL::character varying"))
	language = db.Column(String(128), server_default=text("NULL::character varying"))
	country = db.Column(String(128), server_default=text("NULL::character varying"))
	awards = db.Column(String(128), server_default=text("NULL::character varying"))
	poster = db.Column(String(1000), server_default=text("NULL::character varying"))
	rating = db.Column(Float(53), nullable=False)
	votes = db.Column(String(128), server_default=text("NULL::character varying"))
	imdbid = db.Column(String(128), nullable=False, unique=True)
	kind = db.Column(String(128), server_default=text("NULL::character varying"))
	boxoffice = Column(String(256), server_default=text("NULL::character varying"))
	production = Column(String(256), server_default=text("NULL::character varying"))
	website = Column(String(256), server_default=text("NULL::character varying"))

	actors = db.relationship(u'Actors', secondary='actors_by_movies')

	def __init__(self, *args, **kwargs):
		super(Movies, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Movies %r>' % self.title


class Users(db.Model, CRUD):
	__tablename__ = 'users'

	id = db.Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
	username = db.Column(String(20), nullable=False, unique=True)
	password = db.Column(String(100), nullable=False)
	email = db.Column(String(50), nullable=False, unique=True)
	age = db.Column(Integer)
	fullname = db.Column(String(50), server_default=text("NULL::character varying"))

	movies = db.relationship(u'Movies', secondary='users_watchlist')
	rated_movies = db.relationship(u'UserRating')

	def __init__(self, *args, **kwargs):
		super(Users, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<User %r>' % self.username

	def get_watchlist(self):
		return self.movies


class UserRating(db.Model, CRUD):
	__tablename__ = 'user_ratings'

	id = db.Column(Integer, primary_key=True, server_default=text("nextval('user_ratings_id_seq'::regclass)"))
	user_id = db.Column(ForeignKey(u'users.id'), nullable=False)
	movie_id = db.Column(ForeignKey(u'movies_info.id'), nullable=False)
	ratings = db.Column(Float(53), nullable=False)

	movie = db.relationship(u'Movies')
	user = db.relationship(u'Users')

	def __init__(self, *args, **kwargs):
		super(UserRating, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Movies %r>' % self.movie

            
t_users_watchlist = db.Table(
    'users_watchlist', metadata,
    db.Column('user_id', ForeignKey(u'users.id'), primary_key=True, nullable=False),
    db.Column('movie_id', ForeignKey(u'movies_info.id'), primary_key=True, nullable=False)
)