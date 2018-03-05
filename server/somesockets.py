from threading import Lock

import eventlet
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from config import MONGODB_DB_HOST

eventlet.monkey_patch()


app = Flask(__name__)
socket = SocketIO(app, logger=True, engineio_logger=True,
                  message_queue="redis://")


@socket.on('connect')
def connect():
    emit('my_response', {'data': 'Connected', 'count': 0})


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Socket server")
    parser.add_argument("--deploy", action='store_true')
    args = parser.parse_args()

    MONGODB_HOST = 'mongo' if args.deploy else MONGODB_DB_HOST
    
    socket.run(app, debug=True)
