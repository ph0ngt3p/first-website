import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgres://skpayufzrpgynw:ce9b72d9db840cf9a2d5763f73dac8ae8943c8ffa09dffcb2eb7075484669bbe@ec2-54-83-25-217.compute-1.amazonaws.com:5432/'
database_name = 'd6nbt8ghkah3gh'
postgres2 = 'postgresql://postgres:123@localhost:5432/movies'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name
    # SQLALCHEMY_DATABASE_URI = postgres2
    JWT_HEADER_TYPE = ''
    JWT_HEADER_NAME = 'Token'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)