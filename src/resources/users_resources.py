from MovieDatabaseApp.src.models import Users, Movies, db
from MovieDatabaseApp.src.schema import UsersSchema
from flask import request, make_response, jsonify
from flask_restful import Resource, reqparse
from flask_restful.inputs import boolean
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity,\
							jwt_required, jwt_refresh_token_required
from passlib.hash import sha256_crypt

schema = UsersSchema()

parser = reqparse.RequestParser()

class UserRegistration(Resource):
	def post(self):
		post_data = request.get_json()
		try:
			username_check = Users.query.filter_by(username=post_data.get('username')).count()
			email_check = Users.query.filter_by(email=post_data.get('email')).count()

			if username_check > 0:
				msg = 'Username already existed. Please use a different one.'
				responseObject = {
					'status': 'fail',
					'message': msg
				}
				return responseObject

			elif email_check > 0:
				msg = 'Email already taken. Please use a different one.'
				responseObject = {
					'status': 'fail',
					'message': msg
				}
				return responseObject

			else:

				user = Users(
					username = post_data.get('username'),
					password = sha256_crypt.encrypt((str(post_data.get('password')))),
					email = post_data.get('email')
				)

				db.session.add(user)
				db.session.commit()

				responseObject = {
					'status': 'success',
					'message': 'Successfully registered.',
					'access_token': create_access_token(identity=user.id),
					'refresh_token': create_refresh_token(identity=user.id)
				}
				return responseObject

		except Exception as e:
			responseObject = {
				'status': 'fail',
				'message': '{}'.format(e)
			}
			return responseObject

class User(Resource):
	def post(self):
		post_data = request.get_json()
		try:
			user = Users.query.filter_by(username=post_data.get('username')).first()
			if user and sha256_crypt.verify(post_data.get('password'), user.password):
				responseObject = {
					'status': 'success',
					'access_token': create_access_token(identity=user.id),
					'refresh_token': create_refresh_token(identity=user.id)
				}
				return responseObject

			else:
				responseObject = {
					'status': 'fail',
					'message': 'Invalid credentials. Please try again.'
				}
				return responseObject

		except Exception as e:
			responseObject = {
				'status': 'fail',
				'message': '{}'.format(e)
			}
			return responseObject

	@jwt_required
	def get(self):
		current_user = get_jwt_identity()
		user = Users.query.filter_by(id=current_user)
		result = schema.dump(user, many=True).data
		return result

class UserActions(Resource):
	@jwt_required
	def post(self):
		current_user = get_jwt_identity()
		user = Users.query.filter_by(id=current_user).one()
		action = request.json.get('action', None)
		movie_id = request.json.get('movie_id', None)

		try:
			if action == 'modify_watchlist':
				movie = Movies.query.filter_by(id=movie_id).one()
				if movie not in user.movies:
					user.movies.append(movie)
					db.session.commit()

					msg = 'Added {} to {}\'s watchlist'.format(movie.title, user.username)
					responseObject = {
						'status': 'success',
						'message': msg
					}
					return responseObject

				else:
					user.movies.remove(movie)
					db.session.commit()

					msg = 'Removed {} from {}\'s watchlist'.format(movie.title, user.username)
					responseObject = {
						'status': 'success',
						'message': msg
					}
					return responseObject

		except Exception as e:
			responseObject = {
				'status': 'fail',
				'message': '{}'.format(e)
			}
			return responseObject

class TokenRefresh(Resource):
	@jwt_refresh_token_required
	def get(self):
		current_user = get_jwt_identity()
		responseObject = {
			'status': 'success',
			'new_access_token': create_access_token(identity=current_user)
		}
		return responseObject