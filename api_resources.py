from models import Actors, Movies
from schema import *
from flask_restful import Resource, reqparse
from flask_restful.inputs import boolean
user_schema = UsersSchema()
actor_schema = ActorsSchema()
movie_schema = MoviesSchema()

parser = reqparse.RequestParser()
parser.add_argument('genre', type=str, required=False)
parser.add_argument('year', type=str, required=False)
parser.add_argument('rated', type=str, required=False)
parser.add_argument('id', type=int, required=False)
parser.add_argument('string', type=str, required=False)
parser.add_argument('orderby', type=str, required=False)
parser.add_argument('desc', type=boolean)
parser.add_argument('limit', type=int)

class ActorsList(Resource):
	def get(self):
		args = parser.parse_args(strict=True)
		actors_query = Actors.query.all()

		results = actor_schema.dump(actors_query, many=True).data

		if args['orderby']:
			results['data'] = sorted(results['data'], key=lambda item: item['attributes'][args['orderby']], reverse=args['desc'])
		if args['limit']:
			results['data'] = results['data'][:args['limit']]
		results['total_results'] = len(results['data'])

		return results

class Actor(Resource):
	def get(self, actor_id):
		actors_query = Actors.query.filter_by(id = actor_id)
		results = actor_schema.dump(actors_query, many=True).data
		return results

class ActorsSearch(Resource):
	def get(self):
		args = parser.parse_args(strict=True)
		search_str = '%{0}%'.format(args['string'])
		actors_query = Actors.query.filter(Actors.name.ilike(search_str))

		results = actor_schema.dump(actors_query, many=True).data

		if args['orderby']:
			results['data'] = sorted(results['data'], key=lambda item: item['attributes'][args['orderby']], reverse=args['desc'])
		if args['limit']:
			results['data'] = results['data'][:args['limit']]
		results['total_results'] = len(results['data'])

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
		if args['year']:
			movies_query = Movies.query.filter_by(year = args['year'])
		if args['rated']:
			movies_query = Movies.query.filter_by(rated = args['rated'].upper())
		if args['genre']:
			genre = '%{0}%'.format(args['genre'])
			movies_query = Movies.query.filter(Movies.genre.ilike(genre))

		results = movie_schema.dump(movies_query, many=True).data

		if args['orderby']:
			results['data'] = sorted(results['data'], key=lambda item: item['attributes'][args['orderby']], reverse=args['desc'])
		if args['limit']:
			results['data'] = results['data'][:args['limit']]
		results['total_results'] = len(results['data'])

		return results

class MoviesSearch(Resource):
	def get(self):
		args = parser.parse_args(strict=True)
		search_str = '%{0}%'.format(args['string'])
		movies_query = Movies.query.filter(Movies.title.ilike(search_str))

		results = movie_schema.dump(movies_query, many=True).data

		if args['year']:
			results['data'] = [item for item in results['data'] if item['attributes']['year'] == int(args['year'])]
		if args['rated']:
			results['data'] = [item for item in results['data'] if item['attributes']['rated'] == args['rated'].upper()]
		if args['genre']:
			results['data'] = [item for item in results['data'] if args['genre'].capitalize() in item['attributes']['genre']]
		if args['orderby']:
			results['data'] = sorted(data['data'], key=lambda item: item['attributes'][args['orderby']], reverse=args['desc'])
		if args['limit']:
			results['data'] = results['data'][:args['limit']]
		results['total_results'] = len(results['data'])

		return results

class UsersList(Resource):
	def get(self):
		users_query = Users.query.all()
		results = user_schema.dump(users_query, many=True).data
		return results