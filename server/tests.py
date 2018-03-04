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
        valid_token = loads(response.data.decode('utf-8'))['auth_token']

        response = helper(valid_token)
        self.assertEqual(response[0], 422)
        self.assertEqual(response[1]['error'], "Malformed request")

        data = dict(map=dumps({}))

        response = helper('garbage_token', data['map'])

        self.assertEqual(response[0], 422)
        self.assertEqual(response[1]['error'], "Malformed request")

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
        response = helper(dict(email=valid_user.email), data)

        self.assertEqual(response[0], 200)
        self.assertEqual(response[1]['success'], "Successfully created map")


if __name__ == '__main__':
    unittest.main()
