import eventlet
from eventlet import wsgi
from app import app as application
import os

app = application

PORT = int(os.environ.get('PORT', 8000))
wsgi.server(eventlet.listen(('localhost', PORT+1)), app)