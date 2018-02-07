from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#=====================================================
# SocketIO
#=====================================================

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
	print("a user connected")

@socketio.on('disconnect')
def handle_disconnect():
	print("a user has left")

@socketio.on('update')
def handle_update(json):
	print('received json: ' + str(json))
	emit('update', json)

#TODO: Send this in the event the submitted room code isn't found
def handle_RoomNotFound(json):
	emit('RoomNotFound', json)
	print ('Room Not Found!')

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Socket server for ARTop")
    parser.add_argument("port", type=int, help="The port you want the server to run on", default=5000)
    args = parser.parse_args()

    if args.port < 50:
        print("Port can't be negative or privileged!")
        exit()
    
    socketio.run(app, port=args.port)
