import unittest
from models import *
from helper import *
from server import *
from flask_security import MongoEngineUserDatastore
from somesockets import app, socketio


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
            self.assertEqual(responses['args'][0], correct_response)
            self.assertEqual(responses['name'], event_name)

        # No query string -> Malformed request
        helper('', 'error', 'Malformed request')

        # Query string that makes no sense -> Malformed request
        helper('sdgo', 'error', 'Malformed request')

        url = 'http://127.0.0.1:80/?'
        # Valid query string but room doesn't exist -> roomNotFound
        helper(url + 'code=DNE', 'roomNotFound', 'No session exists for this room code')

        # Session exists and valid query -> Connection event
        valid_room = 'abcde'
        session = Session(user_id=self.user.id,
                          game_map_id=self.map.id,
                          code=valid_room)
        session.save()
        
        helper(url + 'code=' + valid_room, 'connect', dict(message='Another user connected'))
       
if __name__ == "__main__":
    unittest.main()
