import unittest
from flask import Flask
from flask_socketio import SocketIO
from somesockets import app, socketio
from models import Session
from helper import *
from server import *
from flask import current_app, jsonify, request
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security


test_email = "artop@gmail.com"
test_password = "abc123"
user_datastore = MongoEngineUserDatastore(db, User, Role)

class TestSocketIO(unittest.TestCase):
    def setUp(self):
        Session.objects.all().delete()
        User.objects.all().delete()
        GameMap.objects.all().delete()

        user_datastore.create_user(
            email=test_email, password=Helper.hashpw(test_password))
        self.user = User.objects(email=test_email).first()

        self.map = GameMap(owner=self.user.id, name="boi", width=10,
                           height=10, depth=10, color='#fff', private=False, models=[])
        self.map.save()

    def test_connect(self):
        def helper(s, event_name, correct_response):
            client = socketio.test_client(app, query_string=s)
            responses = client.get_received()[0]
            print(responses)
            self.assertEqual(responses['args'][0], correct_response)
            self.assertEqual(responses['args'][0], correct_response)

        # No query string -> Malformed request
        helper('', 'error', 'Malformed request')

        # Query string that makes no sense -> Malformed request
        helper('sdgo', 'error', 'Malformed request')

        url = 'http://127.0.0.1:80/?'
        # Valid query string but room doesn't exist -> roomNotFound
        helper(url + 'code=DNE', 'roomNotFound', 'No session exists for this room code')

        # Session exists and valid query -> Connection event
        session = Session(user_id=self.user.id,
                          game_map_id=self.map.id,
                          code='abcde')
        session.save()

        helper(url + 'code=abcde', 'connect', 'Another user connected')
       
if __name__ == "__main__":
    unittest.main()
