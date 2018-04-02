import sys
from argparse import ArgumentParser
from json import loads
from threading import Lock

import eventlet
from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
from flask_socketio import (SocketIO, close_room, emit, join_room, leave_room,
                            rooms, send)

from models import GameMap, Session

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
    emit('connected', {})


@socket.on('joinRoom')
def join(json):
    try:
        room = json['room']
        session = Session.objects(code=room.lower()).first()
        if session is not None:
            join_room(room.lower())
            # sends a message event
            # send("{} has joined {}".format(request.sid, room), room=room)
            game_map = GameMap.objects(id=session.game_map_id).first()
            game_map = game_map.to_json()
            game_map = loads(game_map)
            name = game_map["name"]
            color = game_map["color"]
            models = game_map["models"]
            width = game_map["width"]
            height = game_map["height"]
            color = game_map["color"]
            depth = game_map["depth"]

            emit('roomFound', {'name': name, 'color': color,
                               'models': models, 'width': width, 'height': height, 'depth': depth})
        else:
            emit('roomNotFound', {'data': 'Room ' + room + ' does not exist.'})
    except KeyError:
        emit('error', {'data': 'Malformed request'})
    except Exception as e:
        app.logger.error(str(e))
        emit('error', {'data': 'Internal server error'})


@socket.on('close_room')
def disconnect(room):
    close_room(room)


# Leave room event should be here but we were unable to get it to work.
# For some reason, flask-socketio was literally switching the type
# of argument we received each time (once it was a string, next it
# was a dict, etc.). We coulnd't fix it.


if __name__ == "__main__":
    socket.run(app, debug=True, host='0.0.0.0', port=80)
