from MovieDatabaseApp.src.model.models import Movies, db, UserRating
from MovieDatabaseApp.src.model.schema import MoviesSchema
from sqlalchemy.sql import func
from flask_restful import Resource, reqparse
from flask_restful.inputs import boolean

schema = MoviesSchema()

parser = reqparse.RequestParser()
parser.add_argument('genre', type=str, required=False)
parser.add_argument('year', type=str, required=False)
parser.add_argument('rated', type=str, required=False)
parser.add_argument('id', type=int, required=False)
parser.add_argument('string', type=str, required=False)
parser.add_argument('orderby', type=str, required=False)
parser.add_argument('desc', type=boolean)
parser.add_argument('limit', type=int)

class Movie(Resource):
	def get(self, movie_id):
		query = Movies.query.filter_by(id = movie_id)
		results = schema.dump(query, many=True).data
		return results

class MoviesList(Resource):
	def get(self):
		args = parser.parse_args(strict=True)
		query = Movies.query.all()
		if args['year']:
			query = Movies.query.filter_by(year = args['year'])
		if args['rated']:
			query = Movies.query.filter_by(rated = args['rated'].upper())
		if args['genre']:
			genre = '%{0}%'.format(args['genre'])
			query = Movies.query.filter(Movies.genre.ilike(genre))

		results = schema.dump(query, many=True).data

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
		query = Movies.query.filter(Movies.title.ilike(search_str))

		results = schema.dump(query, many=True).data

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