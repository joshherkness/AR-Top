import unittest
from flask import Flask
from flask_socketio import SocketIO
from somesockets import app, socketio

class TestSocketIO(unittest.TestCase):
    def test_connect(self):
        # No query string -> Malformed request
        client = socketio.test_client(app)
        responses = client.get_received()
        self.assertEqual(responses[0]['args'], 'Malformed request')

        client = socketio.test_client(app, query_string="DNE")
        responses = client.get_received()
        self.assertEqual(responses[0]['args'], 'Room not found')
        

if __name__ == "__main__":
    unittest.main()
