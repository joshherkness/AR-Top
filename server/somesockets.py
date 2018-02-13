from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#=====================================================
# SocketIO
#=====================================================

socketio = SocketIO(app)
open_rooms = dict()
bijection = dict()


@socketio.on('connect')
def handle_connect(json):
    try:
        room = json['roomNumber']
    except:
        emit('Malformed request')
        return

    if room not in open_rooms:
        emit('RoomNotFound', json)
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
