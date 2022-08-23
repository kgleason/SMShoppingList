from pydoc import cli
from app import app, manager, socketio


@cli.command
def run():
	socketio.run(app, transports='websocket, xhr-polling, xhr-multipart')

app.debug = True

if __name__ == "__main__":
    cli()