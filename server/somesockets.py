from threading import Lock

import sys
import eventlet
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
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


if __name__ == "__main__":
    socket.run(app, debug=True, host='0.0.0.0', port=5001)
