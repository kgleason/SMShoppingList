from flask import Flask
from flask.cli import FlaskGroup
from flask_migrate import Migrate
#from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app)
#socketio.init_app(app, cors_allowed_origins="*")

migrate = Migrate()

db = SQLAlchemy(app=app)

cli = FlaskGroup(app)

migrate.init_app(app, db)
CORS(app)


from app import models, views
