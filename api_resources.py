from models import Actors, ActorsSchema, Movies, MoviesSchema, db
from flask_restful import Resource, reqparse
actor_schema = ActorsSchema()
movie_schema = MoviesSchema()

parser = reqparse.RequestParser()
parser.add_argument('genre', type=str, required=False)
parser.add_argument('id', type=int, required=False)
parser.add_argument('string', type=str, required=False)

class ActorsList(Resource):
	def get(self):
		args = parser.parse_args(strict=True)
		actor_id = args['id']

		if actor_id is None:
			actors_query = Actors.query.all()
		else:
			actors_query = Actors.query.filter_by(id = actor_id)
		results = actor_schema.dump(actors_query, many=True).data
		return results

class ActorsSearch(Resource):
	def get(self):
		args = parser.parse_args(strict=True)

		search_str = '%{0}%'.format(args['string'])

		actors_query = Actors.query.filter(Actors.name.ilike(search_str))
		results = actor_schema.dump(actors_query, many=True).data
		return results

class Movie(Resource):
	def get(self, movie_id):
		movies_query = Movies.query.filter_by(id = movie_id)
		results = movie_schema.dump(movies_query, many=True).data
		return results

class MoviesList(Resource):
	def get(self):
		args = parser.parse_args(strict=True)

		movies_query = Movies.query.all()
		if args['genre']:
			genre = '%{0}%'.format(args['genre'])
			movies_query = Movies.query.filter(Movies.genre.ilike(genre))
		results = movie_schema.dump(movies_query, many=True).data
		return results

class MoviesSearch(Resource):
	def get(self):
		args = parser.parse_args(strict=True)

		search_str = '%{0}%'.format(args['string'])

		movies_query = Movies.query.filter(Movies.title.ilike(search_str))
		results = movie_schema.dump(movies_query, many=True).data
		return results
