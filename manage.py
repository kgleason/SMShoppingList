from app import app, manager, socketio
from flask.ext.migrate import MigrateCommand

manager.add_command('db', MigrateCommand)


@manager.command
def run():
	socketio.run(app, transports='websocket, xhr-polling, xhr-multipart')

app.debug = True

if __name__ == '__main__':
  manager.run()
