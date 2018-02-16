from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from secrets import SOCKETIO_SECRET_KEY
from models import Session
from flask_mongoengine import MongoEngine

#=====================================================
# Global vars
#=====================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = SOCKETIO_SECRET_KEY
app.config.from_object('config')

db = MongoEngine(app)

socketio = SocketIO(app)
open_rooms = dict()
bijection = dict()

#=====================================================
# SocketIO
#=====================================================
@socketio.on('connect')
def handle_connect():
    room = request.query_string.decode()
    if room == "":
        send('Malformed request')
        return

    session = Session.objects(code=room).first()
    if session is None:
        send('Room not found')
        return

    open_rooms[room] += [request.sid]
    bijection[request.sid] = room
    emit('Connect', dict(message="Another user connected"), room=room)


@socketio.on('disconnect')
def handle_disconnect():
    room = bijection[request.sid]
    open_rooms[room].remove(request.sid)
    del bijection[request.sid]
    emit('Disconnect', dict(message="User disconnected"), room=room)


@socketio.on('update')
def handle_update(json):
    try:
        room = json['roomNumber']
        map = json['map']
    except:
        send('Malformed request')
        
    emit('update', json=map, room=room)

    
@socketio.on('changeRoom')
def switch_dungeon(json):
    try:
        room = json['roomNumber']
    except:
        send('Malformed request')
        
    emit('update', json=map, room=room)
    
    
if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Socket server for ARTop")
    parser.add_argument("host", type=str, nargs='?', help="The IP addr you want to listen for", default='127.0.0.1')
    parser.add_argument("port", type=int, nargs='?', help="The port you want the server to run on", default=5000)
    args = parser.parse_args()

    if args.port < 80:
        print("Port can't be negative or privileged!")
        exit()
    
    socketio.run(app, host=args.host, port=args.port)
