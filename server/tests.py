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
            response = self.request(
                '/api/authenticated', auth_data, 'GET', payload)
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
        self.assertEqual(response[1]['user']['_id']
                         ['$oid'], str(valid_user.id))

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
            response = self.request(
                '/api/map/' + map_id, auth_data, 'POST', payload)
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
        test_map = loads(test_map.to_json())
        mapz = {'id': test_map_id, 'name': test_map['name'], 'color': test_map['color'],
                'width': test_map['width'], 'height': test_map['height'], 'depth': test_map['depth']}

        data['map'] = mapz
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
            response = self.request(
                '/api/map/' + map_id, auth_data, 'DELETE', payload)
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

        # returns ({error="Map does not exist"}, 404, json_tag)
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
        response = self.request('/api/map', valid_token,
                                'POST', payload=(data))
        json = loads(response.data.decode('utf-8'))
        map_id = json['map']['_id']['$oid']

        # Create session
        data = dict(map_id=dumps({}))
        data['map_id'] = map_id
        response = self.request(
            '/api/sessions', valid_token, 'POST', payload=(data))
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
            response = self.request(
                '/api/sessions', auth_data, 'POST', payload)
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
        response = self.request('/api/map', valid_token,
                                'POST', payload=(data))
        json = loads(response.data.decode('utf-8'))
        map_id = json['map']['_id']['$oid']

        # Create map with missing name, color, models
        map_missing_fields_dict = dict(width=4, height=5,
                                       depth=6, private=True)
        data = dict(map=dumps({}))
        data['map'] = dumps(map_dict)
        response = self.request('/api/map', valid_token,
                                'POST', payload=(data))
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
        self.assertEqual(response[1]['success'],
                         "Successfully created session")
        test_session_json = response[1]['session']
        self.assertEqual(test_session_json['game_map_id']['$oid'], map_id)
        self.assertEqual(
            test_session_json['user_id']['$oid'], str(valid_user.id))
        self.assertIsNotNone(test_session_json['code'])
        test_session_id = test_session_json['_id']['$oid']
        test_session = Session.objects(id=test_session_id).first()
        self.assertIsNotNone(test_session)

    def test_read_session(self):
        def helper(auth_data, session_id):
            response = self.request('/api/sessions/' + session_id, auth_data, 'GET')
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

        # Create session
        response = self.request('/api/sessions', valid_token, 'POST', dict(map_id=map_id))
        json = loads(response.data.decode('utf-8'))
        test_session_id = json['session']['_id']['$oid']

        # Session does not exist
        garbage_session_id = "507f191e810c19729de860ea"
        response = helper(valid_token, garbage_session_id)
        self.assertEqual(response[0].status_code, 404)
        self.assertEqual(response[1]['error'], "Session does not exist")

        # User does not own session
        response = helper(valid_token2, test_session_id)
        self.assertEqual(response[0].status_code, 404)
        self.assertEqual(response[1]['error'], "Session does not exist")

        # Success
        response = helper(valid_token, test_session_id)
        self.assertEqual(response[0].status_code, 200)
        self.assertEqual(response[1]['success'], "Successfully read session")
        self.assertEqual(response[1]['session']['_id']['$oid'], test_session_id)

    def test_delete_session(self):
        def helper(auth_data, session_id):
            response = self.request('/api/sessions/' + session_id, auth_data, 'DELETE')
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

        # Create session
        response = self.request('/api/sessions', valid_token, 'POST', dict(map_id=map_id))
        json = loads(response.data.decode('utf-8'))
        test_session_id = json['session']['_id']['$oid']

        # User making request does not own the session
        response = helper(valid_token2, test_session_id)
        self.assertEqual(response[0].status_code, 404)
        self.assertEqual(response[1], {'error': 'Session does not exist'})

        # Session with session_id does not exist
        garbage_session_id = "507f191e810c19729de860ea"
        response = helper(valid_token, garbage_session_id)
        self.assertEqual(response[0].status_code, 404)
        self.assertEqual(response[1], {'error': 'Session does not exist'})

        # Success
        response = helper(valid_token, test_session_id)
        self.assertEqual(response[0].status_code, 200)
        self.assertEqual(response[1], {'success': 'Successfully removed session'})
        self.assertIsNone(Session.objects(id=test_session_id).first())

    def test_update_session(self):
        def helper(auth_data, session_id, payload=None):
            response = self.request('/api/sessions/' + session_id, auth_data, 'POST', payload)
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

        # Create new map to update session with
        new_map_dict = dict(name="test_map2", width=4, height=5,
                        depth=6, color='#FFF', private=True, models=[])
        data = dict(map=dumps({}))
        data['map'] = dumps(map_dict)
        response = self.request('/api/map', valid_token, 'POST', payload=(data))
        json = loads(response.data.decode('utf-8'))
        new_map_id = json['map']['_id']['$oid']

        # Create new map to update session with
        new_map_dict = dict(name="test_map2", width=4, height=5,
                        depth=6, color='#FFF', private=True, models=[])
        data = dict(map=dumps({}))
        data['map'] = dumps(map_dict)
        response = self.request('/api/map', valid_token, 'POST', payload=(data))
        json = loads(response.data.decode('utf-8'))
        new_map_id = json['map']['_id']['$oid']

        # Create new map to update session with that the valid_user2 owns
        new_map_dict = dict(name="test_map3", width=4, height=5,
                        depth=6, color='#FFF', private=True, models=[])
        data = dict(map=dumps({}))
        data['map'] = dumps(map_dict)
        response = self.request('/api/map', valid_token2, 'POST', payload=(data))
        json = loads(response.data.decode('utf-8'))
        new_map_id2 = json['map']['_id']['$oid']

        # Create session
        response = self.request('/api/sessions', valid_token, 'POST', dict(map_id=map_id))
        json = loads(response.data.decode('utf-8'))
        test_session_id = json['session']['_id']['$oid']

        # User making request does not own the map that the session is being updated with
        data = dict(map_id=dumps({}))
        data['map_id'] = str(new_map_id)
        response = helper(valid_token2, test_session_id, payload=data)
        self.assertEqual(response[0].status_code, 404)
        self.assertEqual(response[1], {'error': 'Game map does not exist'})

        # Map to update session with does not exist
        garbage_map_id = "507f191e810c19729de860ea"
        data['map_id'] = garbage_map_id
        response = helper(valid_token, test_session_id, payload=data)
        self.assertEqual(response[0].status_code, 404)
        self.assertEqual(response[1], {'error': 'Game map does not exist'}) 

        # User making request does not own the session, but owns the map
        data['map_id'] =  str(new_map_id2)
        response = helper(valid_token2, test_session_id, payload=data)
        self.assertEqual(response[0].status_code, 404)
        self.assertEqual(response[1], {'error': 'Session does not exist'}) 

        # Session does not exist
        data['map_id'] =  str(new_map_id)
        garbage_session_id = "507f191e810c19729de860ea"
        response = helper(valid_token, garbage_session_id, payload=data)
        self.assertEqual(response[0].status_code, 404)
        self.assertEqual(response[1], {'error': 'Session does not exist'}) 

        # Malformed data sent in body
        data = dict(malformed_map_id=dumps({}))
        data['malformed_map_id'] = str(new_map_id)
        response = helper(valid_token, test_session_id, payload=data)
        self.assertEqual(response[0].status_code, 422)
        self.assertEqual(response[1], {'error': 'Malformed request'})

        # Success (need to check that updated map matches id)
        data = dict(map_id=dumps({}))
        data['map_id'] = str(new_map_id)
        response = helper(valid_token, test_session_id, payload=data)
        self.assertEqual(response[0].status_code, 200)
        self.assertEqual(response[1]['success'], "Successfully updated session with new map")
        updated_session = response[1]['session']
        self.assertEqual(updated_session['_id']['$oid'], test_session_id)
        updated_map_id = updated_session['game_map_id']['$oid']
        self.assertEqual(updated_map_id, str(new_map_id))
        # Check that the session in the database was actually updated
        test_session = Session.objects(id=test_session_id).first()
        self.assertEqual(str(test_session.game_map_id), updated_map_id)


if __name__ == '__main__':
    unittest.main()
