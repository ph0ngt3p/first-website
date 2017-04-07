import os
import datetime
from wtforms import Form, BooleanField, TextField, PasswordField, validators

basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://postgres:123@localhost:5432/'
database_name = 'movies'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name
    JWT_HEADER_TYPE = ''
    JWT_HEADER_NAME = 'Token'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)

class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=20)])
	email = TextField('Email Address', [validators.Length(min=6, max=50), validators.Email(message = 'Please enter a valid email.')])
	password = PasswordField('New Password', [
		validators.Length(min=6, max=20),
		validators.Required(),
		validators.EqualTo('confirm', message='Passwords must match')
	])
	confirm = PasswordField('Repeat password')
	accept_tos = BooleanField('I accept the Terms of Service and blahbloh', [validators.Required()])

def Content():
	CONTENT = {"Top genre":["Action", "Animation", "Comedy", "Crime", "Drama", "Mystery"],
                  "abc":[]}

	return CONTENT