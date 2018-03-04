from threading import Lock

import eventlet
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit

eventlet.monkey_patch()


app = Flask(__name__)
socket = SocketIO(app, logger=True, engineio_logger=True,
                  message_queue="redis://")


@socket.on('connect')
def connect():
    emit('my_response', {'data': 'Connected', 'count': 0})


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', debug=True, port=5001)
