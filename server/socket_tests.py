import unittest
from flask import Flask
from flask_socketio import SocketIO
from somesockets import app, socketio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

class TestSocketIO(unittest.TestCase):
    def test_connect(self):
        client = socketio.test_client(app)
        client.emit('connect')
        data = client.get_received()
        print(data)

if __name__ == "__main__":
    unittest.main()
