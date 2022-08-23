import eventlet
from eventlet import wsgi
from app import app
import os

PORT = os.environ.get('PORT', 8000)
wsgi.server(eventlet.listen(('127.0.0.1', PORT)), app)