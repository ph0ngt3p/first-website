from flask import Flask
from db_connection import dbconn

app = Flask(__name__)

POSTGRES = dbconn()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
