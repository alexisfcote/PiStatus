# noinspection PyUnresolvedReferences
from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# noinspection PyUnresolvedReferences
from app import views, models
