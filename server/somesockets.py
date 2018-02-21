from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from secrets import SOCKETIO_SECRET_KEY
from models import Session
from flask_mongoengine import MongoEngine
from urllib.parse import urlparse, parse_qs


#=====================================================
# Data structures
#=====================================================
class PlayerList():
    open_rooms = dict()
    bijection = dict()

    def add_user(self, sid, room):
        if open_rooms.get(room) is None:
            open_rooms[room] = [sid]
            bijection[sid] = [room]
        else:
            open_rooms[room] += [sid]
            bijection[sid] += [room]
            
#=====================================================
# Global vars
#=====================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = SOCKETIO_SECRET_KEY
app.config.from_object('config')

db = MongoEngine(app)

socketio = SocketIO(app)

pl = PlayerList()
#=====================================================
# Error handling
#=====================================================
@socketio.on_error()
def error_handler(e):
    if e is ValueError or e is TypeError:
        send('Malformed request')
    else:
        send('General error, try again')


@socketio.on_error_default
def default_error_handler(e):
    app.logger.error("General error with request.sid=" + request.sid)
    send('Internal server error, try again')
#=====================================================
# Routes
#=====================================================
@socketio.on('connect')
def connect():
    room = request.query_string.decode().lower()
    room = parse_qs(urlparse(room).query)['code']
    room = Session.objects(code=room).first()
    
    if room is None:
        error_handler(ValueError())
    else:
        join_room(room)
        emit('Connect', dict(message="Another user connected"), room=room)

@socketio.on('disconnect')
def disconnect():
    # This function technically doesn't even need to exist;
    # by default socketio handles room disconnection.
    # This is here purely in case we want to do anything additional.
    emit('Disconnect', dict(message="User disconnected"), room=room)

@socketio.on('update')
def handle_update(map, room):
    """
    This isn't a socket event, this is triggered from within the flask application.
    """
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
