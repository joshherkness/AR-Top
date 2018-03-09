import sys
from argparse import ArgumentParser
from threading import Lock

import eventlet
from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO, emit, join_room, send, rooms

from models import Session

parser = ArgumentParser(description="Socket server")
parser.add_argument("--deploy", action='store_true')
args = parser.parse_args()

eventlet.monkey_patch()

app = Flask(__name__)
app.config['MONGODB_DB'] = 'mydatabase'
app.config['MONGODB_PORT'] = 27017


if args.deploy:
    socket = SocketIO(app, logger=True, engineio_logger=True,
                      message_queue="redis://redis")
    app.config['MONGODB_HOST'] = 'mongo'
    db = MongoEngine(app)
else:
    socket = SocketIO(app, logger=True, engineio_logger=True,
                      message_queue="redis://")
    app.config['MONGODB_HOST'] = 'localhost'
    db = MongoEngine(app)


@socket.on('connect')
def connect():
    send("{} has connected".format(request.sid))


@socket.on('joinRoom')
def join(json):
    try:
        room = json['room']
        if Session.objects(code=room.lower()).first() is not None:
            join_room(room.lower())
            # sends a message event
            send("{} has joined {}".format(request.sid, room), room=room)
        else:
            emit('roomNotFound', {'data': 'Room ' + room + ' does not exist.'})
    except KeyError:
        emit('error', {'data': 'Malformed request'})
    except Exception as e:
        app.logger.error(str(e))
        emit('error', {'data': 'Internal server error'})


if __name__ == "__main__":
    socket.run(app, debug=True, host='0.0.0.0', port=5001)
