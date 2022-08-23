import eventlet
from eventlet import wsgi
from app import app
import os

PORT = os.environ.get('PORT', 8000)
wsgi.server(eventlet.listen(('0.0.0.0', PORT)), app)