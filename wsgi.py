import eventlet
from eventlet import wsgi
from app import app
import os

PORT = int(os.environ.get('PORT', 8000))
wsgi.server(eventlet.listen(('localhost', PORT)), app)