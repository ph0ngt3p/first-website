from flask_restless import APIManager
from application import app
from models import Actors, Movies, Users, db

manager = APIManager(app, flask_sqlalchemy_db=db)
movies_blueprint = manager.create_api_blueprint(Movies, collection_name = 'movies', methods=['GET'])
actors_blueprint = manager.create_api_blueprint(Actors, collection_name = 'actors', methods=['GET'])
users_blueprint = manager.create_api_blueprint(Users, collection_name = 'users', methods=['GET'])