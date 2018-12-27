from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
from flask_socketio import SocketIO
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

socketio = SocketIO(app)

db = SQLAlchemy(app=app)

migrate = Migrate(app, db)
manager = Manager(app)

from app import models, views
