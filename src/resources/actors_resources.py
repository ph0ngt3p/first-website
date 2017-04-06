from MovieDatabaseApp.src.models import Actors
from MovieDatabaseApp.src.schema import ActorsSchema
from flask_restful import Resource, reqparse
from flask_restful.inputs import boolean
schema = ActorsSchema()

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, required=False)
parser.add_argument('string', type=str, required=False)
parser.add_argument('orderby', type=str, required=False)
parser.add_argument('desc', type=boolean)
parser.add_argument('limit', type=int)

class ActorsList(Resource):
	def get(self):
		args = parser.parse_args(strict=True)
		query = Actors.query.all()

		results = schema.dump(query, many=True).data

		if args['orderby']:
			results['data'] = sorted(results['data'], key=lambda item: item['attributes'][args['orderby']], reverse=args['desc'])
		if args['limit']:
			results['data'] = results['data'][:args['limit']]
		results['total_results'] = len(results['data'])

		return results

class Actor(Resource):
	def get(self, actor_id):
		query = Actors.query.filter_by(id = actor_id)
		results = schema.dump(query, many=True).data
		return results

class ActorsSearch(Resource):
	def get(self):
		args = parser.parse_args(strict=True)
		search_str = '%{0}%'.format(args['string'])
		query = Actors.query.filter(Actors.name.ilike(search_str))

		results = schema.dump(query, many=True).data

		if args['orderby']:
			results['data'] = sorted(results['data'], key=lambda item: item['attributes'][args['orderby']], reverse=args['desc'])
		if args['limit']:
			results['data'] = results['data'][:args['limit']]
		results['total_results'] = len(results['data'])

		return results