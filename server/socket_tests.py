import unittest
from flask import Flask
from flask_socketio import SocketIO
from somesockets import app, socketio
from models import Session

class TestSocketIO(unittest.TestCase):
    def setUp(self):
        Session.objects.all().delete()
    
    def test_connect(self):
        def helper(s, event_name, correct_response):
            client = socketio.test_client(app, query_string=s)
            responses = client.get_received()[0]
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
        session = Session(user='012345678901234567890123',
                          map='012345678901234567890123',
                          code='abcde')
        session.save()

        helper(url + 'code=abcde', 'connect', 'Another user connected')
       
if __name__ == "__main__":
    unittest.main()
