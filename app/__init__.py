from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
application = Flask(__name__)
application.config.from_object('config')
application.secret_key = 'some_secret'
db = SQLAlchemy(application)
from app import views, models
