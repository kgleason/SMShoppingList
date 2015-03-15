from app import app, manager, socketio
from flask.ext.migrate import MigrateCommand

manager.add_command('db', MigrateCommand)

app.debug = True

if __name__ == '__main__':
  socketio.run(app)
