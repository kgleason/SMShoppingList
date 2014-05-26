from app import app, manager
from flask.ext.migrate import MigrateCommand

manager.add_command('db', MigrateCommand)

app.debug = True

if __name__ == '__main__':
  manager.run()
