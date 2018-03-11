import os
import tempfile
import unittest

import bcrypt
import base64
import jwt
from json import dumps, loads
from flask import Blueprint
from server import app, api
from secrets import JWT_KEY
from models import GameMap, User, Session, Role
from constants import max_email_length, max_password_length
from flask_security import MongoEngineUserDatastore
from flask_mongoengine import MongoEngine


class TestApp(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['MONGODB_DB'] = 'test'
        app.config['DEBUG'] = False
        app.testing = True
        app.register_blueprint(api)
        self.client = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        GameMap.objects.all().delete()
        User.objects.all().delete()
        Session.objects.all().delete()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def request(self, page, auth_data=None, method='POST', payload=None, content_type="application/json"):
        headers = {
            'Authorization': 'Bearer ' + jwt.encode(dict(data=auth_data), base64.b64decode(JWT_KEY), algorithm='HS512').decode()
        }
        response = self.client.open(
            page, method=method, data=dumps(payload), follow_redirects=True, headers=headers, content_type=content_type)
        return response

    def test_register(self):
        def helper(data):
            response = self.request('/api/register', data, 'POST')
            json = loads(response.data.decode('utf-8'))
            return response.status_code, json

        # Improper data keys
        data = dict(email="malformed", passwd="request")
        response = helper(data)
        self.assertEqual(response[0], 422)
        self.assertEqual(response[1]['error'], "Malformed request")

        data = dict(email="a" * (max_email_length + 1),
                    password="email too long")
        response = helper(data)
        self.assertEqual(response[0], 422)
        self.assertEqual(response[1]['error'], "Malformed request")

        # Invalid email
        data = dict(email="a" * (max_email_length + 1),
                    password="email too long")
        response = helper(data)
        self.assertEqual(response[0], 422)

        # Invalid email
        for i in ["bad email1", "badEmail@2", ""]:
            data = dict(email=i, password="something")
            response = helper(data)
            self.assertEqual(response[0], 422)
            self.assertEqual(response[1]['error'], "Malformed request")

        data = dict(email="test@gmail.com", password="testpassword")
        response = helper(data)
        self.assertEqual(response[0], 200)
        self.assertEqual(
            response[1]['success'], "Account has been created! Check your email to validate your account.")

        data = dict(email="new1Emai2lNo24bo5dyShouldHave@gmail.com",
                    password="validPassword123")
        response = helper(data)
        self.assertEqual(response[0], 200)
        self.assertEqual(
            response[1]['success'], "Account has been created! Check your email to validate your account.")

    def test_authenticate(self):
        def helper(data):
            response = self.request('/api/auth', data, 'POST')
            json = loads(response.data.decode('utf-8'))
            return response.status_code, json

        valid_email = "validEmail@gmail.com"
        valid_password = "validPassword123"
        encrypted_password = bcrypt.hashpw(
            valid_password.encode(), bcrypt.gensalt())
        User(email=valid_email, password=encrypted_password).save()
        valid_user = User.objects(email=valid_email).first()

        data = dict(email=valid_email, password=valid_password)
        response = helper(data)
        self.assertEqual(response[0], 200)
        self.assertEqual(response[1]['email'], valid_email)
        self.assertIsNotNone(
            valid_user.verify_auth_token(response[1]['auth_token']))
        self.assertEqual(True, True)

        # wrong password
        data['password'] = 'invalidPassword'
        response = helper(data)

        self.assertEqual(response[0], 200)
        self.assertIsNone(response[1]['auth_token'])

        # wrong email
        data['email'] = 'invalid@email.com'
        data['password'] = valid_password

        response = helper(data)
        self.assertEqual(response[0], 422)
        self.assertEqual(response[1]['error'], "Incorrect email or password")

        data['password'] = 'invalidPassword'

        response = helper(data)
        self.assertEqual(response[0], 422)
        self.assertEqual(response[1]['error'], "Incorrect email or password")

    def test_authenticated(self):
        def helper(auth_data, payload=None):
            response = self.request('/api/authenticated', auth_data, 'GET', payload)
            json = loads(response.data.decode('utf-8'))
            return response.status_code, json
        
        # Create user
        valid_email = "validEmail@gmail.com"
        valid_password = "validPassword123"
        encrypted_password = bcrypt.hashpw(
            valid_password.encode(), bcrypt.gensalt())
        User(email=valid_email, password=encrypted_password).save()
        valid_user = User.objects(email=valid_email).first()

        # Get token
        response = self.request('/api/auth', dict(email=valid_email,
                                                  password=valid_password), 'POST')
        valid_token = loads(response.data.decode('utf-8'))

        # valid token
        response = helper(valid_token)
        self.assertEqual(response[0], 200)
        self.assertEqual(response[1]['user']['_id']['$oid'], str(valid_user.id)) 

        # missing token
        response = helper('')
        self.assertEqual(response[0], 401)
        self.assertEqual(response[1], {'error': 'token expired.'})

        # token invalid
        response = helper('garbage_token')
        self.assertEqual(response[0], 401)
        self.assertEqual(response[1], {'error': 'token expired.'})

    def test_create_map(self):
        def helper(auth_data, payload=None):
            response = self.request('/api/map', auth_data, 'POST', payload)
            json = loads(response.data.decode('utf-8'))
            return response.status_code, json

        # Create user
        valid_email = "validEmail@gmail.com"
        valid_password = "validPassword123"
        encrypted_password = bcrypt.hashpw(
            valid_password.encode(), bcrypt.gensalt())
        User(email=valid_email, password=encrypted_password).save()
        valid_user = User.objects(email=valid_email).first()

        # Get token
        response = self.request('/api/auth', dict(email=valid_email,
                                                  password=valid_password), 'POST')
        valid_token = loads(response.data.decode('utf-8'))

        response = helper(valid_token)
        self.assertEqual(response[0], 422)
        self.assertEqual(response[1]['error'], "Malformed request")

        data = dict(map=dumps({}))

        response = helper('garbage_token', data['map'])

        self.assertEqual(response[0], 401)
        self.assertEqual(response[1]['error'], "token expired.")

        map_dict = dict(name="test_map", width=4, height=5,
                        depth=6, private=True, models=[])
        data['map'] = dumps(map_dict)

        # Missing color key
        response = helper(valid_token, data)
        self.assertEqual(response[0], 422)
        self.assertEqual(response[1]['error'], "Malformed request")

        # With color key
        map_dict['color'] = "#fff"
        data['map'] = dumps(map_dict)
        response = helper(valid_token, data)

        self.assertEqual(response[0], 200)
        self.assertEqual(response[1]['success'], "Successfully created map")

    def test_update_map(self):
        def helper(auth_data, map_id, payload=None):
            response = self.request('/api/map/' + map_id, auth_data, 'POST', payload)
            json = loads(response.data.decode('utf-8'))
            return response.status_code, json

        # Create user
        valid_email = "validEmail@gmail.com"
        valid_password = "validPassword123"
        encrypted_password = bcrypt.hashpw(
            valid_password.encode(), bcrypt.gensalt())
        User(email=valid_email, password=encrypted_password).save()
        valid_user = User.objects(email=valid_email).first()

        # Get token
        response = self.request('/api/auth', dict(email=valid_email,
                                                  password=valid_password), 'POST')
        valid_token = loads(response.data.decode('utf-8'))

        # Create second user
        valid_email2 = "secondEmail@gmail.com"
        valid_password2 = "secondPassword123"
        encrypted_password2 = bcrypt.hashpw(
            valid_password2.encode(), bcrypt.gensalt())
        User(email=valid_email2, password=encrypted_password2).save()
        valid_user2 = User.objects(email=valid_email2).first()

        # Get second token
        response = self.request('/api/auth', dict(email=valid_email2,
                                                  password=valid_password2), 'POST')
        valid_token2 = loads(response.data.decode('utf-8'))

        # Create map
        map_dict = dict(name="test_map", width=4, height=5,
                        depth=6, color="#fff", private=True, models=[])
        data = dict(map=dumps({}))
        data['map'] = dumps(map_dict)
        response = self.request('/api/map', valid_token, 'POST', data)
        json = loads(response.data.decode('utf-8'))
        test_map_id = json['map']['_id']['$oid']
        test_map = GameMap.objects(id=test_map_id).first()

        # Success
        #map = request.json['map']
        data = dict(map=dumps({}))
        data['map'] = json['map']
        response = helper(valid_token, test_map_id, data)
        self.assertEqual(response[0], 200)
        self.assertEqual(response[1]['map']['name'], json['map']['name'])
        self.assertEqual(response[1]['map']['color'], json['map']['color'])
        self.assertEqual(response[1]['map']['width'], json['map']['width'])
        self.assertEqual(response[1]['map']['height'], json['map']['height'])
        self.assertEqual(response[1]['map']['depth'], json['map']['depth'])
        self.assertEqual(response[1]['map']['private'], json['map']['private'])
        self.assertEqual(response[1]['map']['models'], json['map']['models'])
        self.assertEqual(response[1]['map']['_id'], json['map']['_id'])

        # user making the request does not own the map with map_id
        response = helper(valid_token2, test_map_id, data)
        self.assertEqual(response[0], 404)
        self.assertEqual(response[1], {'error': 'Map does not exist'})

        # map with map_id does not exist
        garbage_map_id = "507f191e810c19729de860ea"
        response = helper(valid_token, garbage_map_id, data)
        self.assertEqual(response[0], 404)
        self.assertEqual(response[1], {'error': 'Map does not exist'})

        # The new map json sent in the body is improperly formatted.
        # (if the color value doesn't change, we know it was invalid
        #   invalid json doesn't throw an error, the field that is invalid 
        #   isn't changed in the database)
        invalid_color = 'not a color string'
        data['color'] = invalid_color
        response = helper(valid_token, test_map_id, data)
        self.assertEqual(response[0], 200)
        self.assertNotEqual(response[1]['map']['color'], invalid_color)

    def test_delete_map(self):
        def helper(auth_data, map_id, payload=None):
            response = self.request('/api/map/' + map_id, auth_data, 'DELETE', payload)
            json = loads(response.data.decode('utf-8'))
            return response.status_code, json

        # Create user
        valid_email = "validEmail@gmail.com"
        valid_password = "validPassword123"
        encrypted_password = bcrypt.hashpw(
            valid_password.encode(), bcrypt.gensalt())
        User(email=valid_email, password=encrypted_password).save()
        valid_user = User.objects(email=valid_email).first()

        # Get token
        response = self.request('/api/auth', dict(email=valid_email,
                                                  password=valid_password), 'POST')
        valid_token = loads(response.data.decode('utf-8'))

        # Create second user
        valid_email2 = "secondEmail@gmail.com"
        valid_password2 = "secondPassword123"
        encrypted_password2 = bcrypt.hashpw(
            valid_password2.encode(), bcrypt.gensalt())
        User(email=valid_email2, password=encrypted_password2).save()
        valid_user2 = User.objects(email=valid_email2).first()

        # Get second token
        response = self.request('/api/auth', dict(email=valid_email2,
                                                  password=valid_password2), 'POST')
        valid_token2 = loads(response.data.decode('utf-8'))

        # Create map
        map_dict = dict(name="test_map", width=4, height=5,
                        depth=6, color="#fff", private=True, models=[])
        data = dict(map=dumps({}))
        data['map'] = dumps(map_dict)
        response = self.request('/api/map', valid_token, 'POST', data)
        json = loads(response.data.decode('utf-8'))
        test_map_id = json['map']['_id']['$oid']
        test_map = GameMap.objects(id=test_map_id).first()

        # returns ({error="Map does not exist"}, 404, json_tag) 
        # user making the request does not own the map with map_id
        response = helper(valid_token2, test_map_id)
        self.assertEqual(response[0], 404)
        self.assertEqual(response[1], {'error': 'Map does not exist'})

        #returns ({error="Map does not exist"}, 404, json_tag)
        # if a map with map_id does not exist
        garbage_map_id = "507f191e810c19729de860ea"
        response = helper(valid_token, garbage_map_id)
        self.assertEqual(response[0], 404)
        self.assertEqual(response[1], {'error': 'Map does not exist'})

        # Success
        response = helper(valid_token, test_map_id)
        self.assertEqual(response[0], 200)
        self.assertEqual(response[1], {'success': test_map_id})
        self.assertIsNone(GameMap.objects(id=test_map_id).first())


    def test_read_session_user_id(self):
        def helper(auth_data, payload=None):
            response = self.request('/api/sessions', auth_data, 'GET', payload)
            json = loads(response.data.decode('utf-8'))
            return response, json
        
        # Create user
        valid_email = "validEmail@gmail.com"
        valid_password = "validPassword123"
        encrypted_password = bcrypt.hashpw(
            valid_password.encode(), bcrypt.gensalt())
        User(email=valid_email, password=encrypted_password).save()
        valid_user = User.objects(email=valid_email).first()

        # Get token
        response = self.request('/api/auth', dict(email=valid_email,
                                                  password=valid_password), 'POST')
        valid_token = loads(response.data.decode('utf-8'))
        response = helper(valid_token)
        self.assertEqual(response[0].status_code, 404)
        self.assertEqual(response[1], {'error': 'Session does not exist'})

        # Create map
        map_dict = dict(name="test_map", width=4, height=5,
                        depth=6, color='#FFF', private=True, models=[])
        data = dict(map=dumps({}))
        data['map'] = dumps(map_dict)
        response = self.request('/api/map', valid_token, 'POST', payload=(data))
        json = loads(response.data.decode('utf-8'))
        map_id = json['map']['_id']['$oid']

        # Create session
        data = dict(map_id=dumps({}))
        data['map_id'] = map_id
        response = self.request('/api/sessions', valid_token, 'POST', payload=(data))
        json = loads(response.data.decode('utf-8'))
        session_json = json['session']
        session_id = json['session']['_id']['$oid']

        # Start testing
        response, json = helper(valid_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('session' in json, True)
        self.assertEqual('success' in json, True)
        self.assertEqual(json['session'], session_json)
        self.assertEqual(json['success'], 'Successfully read session')

    def test_create_session(self):
        def helper(auth_data, payload=None):
            response = self.request('/api/sessions', auth_data, 'POST', payload)
            json = loads(response.data.decode('utf-8'))
            return response, json
        
        # Create user
        valid_email = "validEmail@gmail.com"
        valid_password = "validPassword123"
        encrypted_password = bcrypt.hashpw(
            valid_password.encode(), bcrypt.gensalt())
        User(email=valid_email, password=encrypted_password).save()
        valid_user = User.objects(email=valid_email).first()

        # Get token
        response = self.request('/api/auth', dict(email=valid_email,
                                                  password=valid_password), 'POST')
        valid_token = loads(response.data.decode('utf-8'))

        # Create second user
        valid_email2 = "secondEmail@gmail.com"
        valid_password2 = "secondPassword123"
        encrypted_password2 = bcrypt.hashpw(
            valid_password2.encode(), bcrypt.gensalt())
        User(email=valid_email2, password=encrypted_password2).save()
        valid_user2 = User.objects(email=valid_email2).first()

        # Get second token
        response = self.request('/api/auth', dict(email=valid_email2,
                                                  password=valid_password2), 'POST')
        valid_token2 = loads(response.data.decode('utf-8'))


        # Create map
        map_dict = dict(name="test_map", width=4, height=5,
                        depth=6, color='#FFF', private=True, models=[])
        data = dict(map=dumps({}))
        data['map'] = dumps(map_dict)
        response = self.request('/api/map', valid_token, 'POST', payload=(data))
        json = loads(response.data.decode('utf-8'))
        map_id = json['map']['_id']['$oid']

        # Create map with missing name, color, models
        map_missing_fields_dict = dict(width=4, height=5,
                        depth=6, private=True)
        data = dict(map=dumps({}))
        data['map'] = dumps(map_dict)
        response = self.request('/api/map', valid_token, 'POST', payload=(data))
        json = loads(response.data.decode('utf-8'))
        map_missing_fields_id = json['map']['_id']['$oid']

        # Missing map_id
        response = helper(valid_token)
        self.assertEqual(response[0].status_code, 422)
        self.assertEqual(response[1], {'error': 'Malformed request'})

        # Invalid map_id
        response = helper(valid_token, dict(map=dict(malformed='asdf')))
        self.assertEqual(response[0].status_code, 422)
        self.assertEqual(response[1], {'error': 'Malformed request'})

        # Map with map_id does not exist
        missing_map_id = "507f191e810c19729de860ea"
        response = helper(valid_token, dict(map_id=missing_map_id))
        self.assertEqual(response[0].status_code, 404)
        self.assertEqual(response[1], {'error': 'Map does not exist'})

        # User does not own the map with map_id
        response = helper(valid_token2, dict(map_id=map_id))
        self.assertEqual(response[0].status_code, 404)
        self.assertEqual(response[1], {'error': 'Map does not exist'})

        # Success
        response = helper(valid_token, dict(map_id=map_id))
        self.assertEqual(response[0].status_code, 200)
        self.assertEqual(response[1]['success'], "Successfully created session")
        test_session_json = response[1]['session']
        self.assertEqual(test_session_json['game_map_id']['$oid'], map_id)
        self.assertEqual(test_session_json['user_id']['$oid'], str(valid_user.id))
        self.assertIsNotNone(test_session_json['code'])
        test_session_id = test_session_json['_id']['$oid']
        test_session = Session.objects(id=test_session_id).first()
        self.assertIsNotNone(test_session)



if __name__ == '__main__':
    unittest.main()
