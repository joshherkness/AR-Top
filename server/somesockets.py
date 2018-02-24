from secrets import SOCKETIO_SECRET_KEY
from urllib.parse import parse_qs, urlparse

from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO, emit, send

import models  # import like this or you'll get circular dependencies

#=====================================================
# Global vars
#=====================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = SOCKETIO_SECRET_KEY
app.config.from_object('config')

db = MongoEngine(app)

socketio = SocketIO(app)


#=====================================================
# Error handling
#=====================================================
@socketio.on_error()
def error_handler(e):
    if type(e) in [ValueError, TypeError]:
        emit('error', 'Malformed request')
    else:
        print(e)
        emit('error', 'General error, try again')


@socketio.on_error_default
def default_error_handler(e):
    app.logger.error("General error with request.sid=" + request.sid)
    emit('error', 'Internal server error, try again')


#=====================================================
# Routes
#=====================================================
@socketio.on('connect')
def connect():
    code = request.query_string.decode().lower()
    code = parse_qs(urlparse(code).query)
    if code.get('code') is None:
        error_handler(ValueError('Invalid room code'))
        return

    code = models.Session.objects(code=code['code']).first()
    if code is None:
        emit('roomNotFound', 'No session exists for this room code')
        return

    join_room(code)
    emit('connect', dict(message="Another user connected"), room=code)


@socketio.on('disconnect')
def disconnect():
    # This function technically doesn't even need to exist;
    # by default socketio handles room disconnection.
    # This is here purely in case we want to do anything additional.
    pass


@socketio.on('update')
def update(map_id, room):
    """
    This isn't a socket event, this is triggered from within the flask application.
    Nobody should be hitting this endpoint.
    """
    map = models.GameMap.objects(id=map_id).first()
    emit('update', json=dict(map=map), room=room)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Socket server for ARTop")
    parser.add_argument("host", type=str, nargs='?',
                        help="The IP addr you want to listen for", default='0.0.0.0')
    parser.add_argument("port", type=int, nargs='?',
                        help="The port you want the server to run on", default=5001)
    args = parser.parse_args()

    if args.port < 80:
        print("Port can't be negative or privileged!")
        exit()

    socketio.run(app, host=args.host, port=args.port)
