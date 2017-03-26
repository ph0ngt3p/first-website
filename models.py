# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

metadata = db.metadata

t_actors_by_movies = db.Table(
    'actors_by_movies', metadata,
    db.Column('movie_id', ForeignKey(u'movies_info.id'), primary_key=True, nullable=False),
    db.Column('actor_id', ForeignKey(u'actors_info.id'), primary_key=True, nullable=False)
)


class Actors(db.Model):
    __tablename__ = 'actors_info'

    id = db.Column(Integer, primary_key=True, server_default=text("nextval('actors_info_id_seq'::regclass)"))
    aka = db.Column(String(250), server_default=text("NULL::character varying"))
    biography = db.Column(String(5000), server_default=text("NULL::character varying"))
    birthday = db.Column(String(128), server_default=text("NULL::character varying"))
    deathday = db.Column(String(128), server_default=text("NULL::character varying"))
    gender = db.Column(String(128), server_default=text("NULL::character varying"))
    homepage = db.Column(String(250), server_default=text("NULL::character varying"))
    tmdbid = db.Column(Integer, nullable=False, unique=True)
    imdbid = db.Column(String(128), server_default=text("NULL::character varying"))
    name = db.Column(String(250), server_default=text("NULL::character varying"))
    place_of_birth = db.Column(String(250), server_default=text("NULL::character varying"))
    profile_pic = db.Column(String(500), server_default=text("NULL::character varying"))

    def __init__(self, *args, **kwargs):
        super(Actors, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Actors %r>' % self.name


class Movies(db.Model):
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
    plot = db.Column(String(1000), server_default=text("NULL::character varying"))
    language = db.Column(String(128), server_default=text("NULL::character varying"))
    country = db.Column(String(128), server_default=text("NULL::character varying"))
    awards = db.Column(String(128), server_default=text("NULL::character varying"))
    poster = db.Column(String(1000), server_default=text("NULL::character varying"))
    rating = db.Column(String(128), server_default=text("NULL::character varying"))
    votes = db.Column(String(128), server_default=text("NULL::character varying"))
    imdbid = db.Column(String(128), nullable=False, unique=True)
    kind = db.Column(String(128), server_default=text("NULL::character varying"))

    actors = db.relationship(u'Actors', secondary='actors_by_movies')

    def __init__(self, *args, **kwargs):
        super(Movies, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Movies %r>' % self.title


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    username = db.Column(String(20), nullable=False, unique=True)
    password = db.Column(String(100), nullable=False)
    email = db.Column(String(50), nullable=False, unique=True)
    profile_pic = db.Column(String(1000), server_default=text("NULL::character varying"))
    fname = db.Column(String(20), server_default=text("NULL::character varying"))
    lname = db.Column(String(20), server_default=text("NULL::character varying"))
    age = db.Column(Integer)

    movies = db.relationship(u'Movies', secondary='users_watchlist')

    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User %r>' % self.username

t_users_watchlist = db.Table(
    'users_watchlist', metadata,
    db.Column('user_id', ForeignKey(u'users.id'), primary_key=True, nullable=False),
    db.Column('movie_id', ForeignKey(u'movies_info.id'), primary_key=True, nullable=False)
)