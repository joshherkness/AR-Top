from threading import Lock

import sys
import eventlet
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit, join_room
from argparse import ArgumentParser
parser = ArgumentParser(description="Socket server")
parser.add_argument("--deploy", action='store_true')
args = parser.parse_args()

eventlet.monkey_patch()

app = Flask(__name__)

if args.deploy:
    socket = SocketIO(app, logger=True, engineio_logger=True,
                      message_queue="redis://redis")
else:
    socket = SocketIO(app, logger=True, engineio_logger=True,
                      message_queue="redis://")


@socket.on('connect')
def connect():
    emit('my_response', {'data': 'Connected', 'count': 0})

@socket.on('joinRoom')
def join_room(json):
    try:
        room = json['room']
        if Session.objects(code=room).first() is not None:
            join_room(room)
            emit('joinRoom', {'data': 'Successfully connected to room ' + room})
        else:
            emit('roomNotFound', {'data':'Room ' + room + ' does not exist.'})
    except KeyError:
        emit('error', {'data':'Malformed request'})
    except:
        emit('error', {'data':'Internal server error'})

if __name__ == "__main__":
    socket.run(app, debug=True, host='0.0.0.0', port=5001)
