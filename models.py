# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
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

    movies = db.relationship(u'Movies', secondary='actors_by_movies')

    def __init__(self, aka, biography, birthday, deathday, gender, homepage, tmdbid, imdbid, name, place_of_birth, profile_pic):
        self.aka = aka
        self.biography = biography
        self.birthday = birthday
        self.deathday = deathday
        self.gender = gender
        self.homepage = homepage
        self.tmdbid = tmdbid
        self.imdbid = imdbid
        self.name = name
        self.place_of_birth = place_of_birth
        self.profile_pic = profile_pic

    def __repr__(self):
        return '<Actor %r>' % self.name


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

    users = db.relationship(u'Users', secondary='users_watchlist')

    def __init__(self, title, year, rated, released, runtime, genre, director, writer, casts, plot, votes, poster):
        self.title = title
        self.year = year
        self.rated = rated
        self.released = released
        self.runtime = runtime
        self.genre = genre
        self.director = director
        self.writer = writer
        self.casts = casts
        self.plot = plot
        self.poster = poster

    def __repr__(self):
        return '<Movie %r>' % self.Title

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    username = db.Column(String(20), unique=True, server_default=text("NULL::character varying"))
    password = db.Column(String(100), server_default=text("NULL::character varying"))
    email = db.Column(String(50), unique=True, server_default=text("NULL::character varying"))
    settings = db.Column(String(32000), server_default=text("NULL::character varying"))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

t_users_watchlist = db.Table(
    'users_watchlist', metadata,
    db.Column('user_id', ForeignKey(u'users.id'), primary_key=True, nullable=False),
    db.Column('movie_id', ForeignKey(u'movies_info.id'), primary_key=True, nullable=False)
)

