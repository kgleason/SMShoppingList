from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate
from flask.ext.socketio import SocketIO
from config import CONFIG

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['DBURI']

socketio = SocketIO(app)

db = SQLAlchemy()
db.app = app
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

from app import models, views
