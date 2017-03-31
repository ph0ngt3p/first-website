from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from models import Actors, Movies, Users

class ActorsSchema(Schema):
	id = fields.Integer(dump_only=True)
	aka = fields.String()
	biography = fields.String()
	birthday = fields.String()
	deathday = fields.String()
	gender = fields.String()
	homepage = fields.String()
	tmdbid = fields.String()
	imdbid = fields.String()
	name = fields.String()
	place_of_birth = fields.String()
	popularity = fields.Float()
	profile_pic = fields.String()

	movies = fields.Nested('MoviesSchema', many=True, exclude=('actors', ), only=('id', 'title'), dump_to='known_for')

	class Meta:
		type_ = 'actor'
		ordered = True

class MoviesSchema(Schema):
	id = fields.Integer(dump_only=True)
	title = fields.String()
	year = fields.Integer()
	rated = fields.String()
	released = fields.String()
	runtime = fields.String()
	genre = fields.String()
	director = fields.String()
	writer = fields.String()
	casts = fields.String()
	plot = fields.String()
	language = fields.String()
	country = fields.String()
	awards = fields.String()
	poster = fields.String()
	rating = fields.Float()
	votes = fields.String()
	imdbid = fields.String()
	kind = fields.String()
	boxoffice = fields.String()
	production = fields.String()
	website = fields.String()

	actors = fields.Nested(ActorsSchema, many=True, only=('id', 'name'))

	class Meta:
		type_ = 'movie'
		ordered = True

class UsersSchema(Schema):
	not_blank = validate.Length(min=1, error='Field cannot be blank')
	id = fields.Integer(dump_only=True)
	username = fields.String(validate=not_blank)
	password = fields.String(validate=not_blank)
	email = fields.Email(validate=not_blank)
	age = fields.String()
	fullname = fields.String()

	movies = fields.Nested(MoviesSchema, many=True, only=('id', 'title'), dump_to='watchlist')

	class Meta:
		type_ = 'user'
		ordered = True
