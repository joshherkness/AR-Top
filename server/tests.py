import os
import unittest
from server import *
import tempfile
from json import loads, dumps
import bcrypt

class TestUserEndpoints(unittest.TestCase):
    #=====================================================
    # Skeleton (you can fold this code)
    #=====================================================
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()
  
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    #=====================================================
    # Helper methods
    #=====================================================
    def request(self, page, data):
        response = self.app.post(page, data=data, follow_redirects=True)
        json = loads(response.data.decode('utf-8'))
        return json, response.status_code
        
    #=====================================================
    # Tests
    #=====================================================
    def test_register(self):
        def tester(data, string, correct_code=422, key='error'):
            response, code = self.request('api/register', data)
            assert code == correct_code
            assert response[key] == string

        data = dict(email="malformed", passwd="request")
        tester(data, "Malformed request; expecting email and password")

        data = dict(email="a" * (max_email_length + 1), password="email too long")
        tester(data, "Email can't be over " + str(max_email_length) + " characters.")

        for i in ["bad email1", "badEmail@2", ""]:
            data = dict(email=i, password="something")
            tester(data, "Email not valid.")

        data = dict(email="valid@email.com", password="tooshrt")
        tester(data, "Password must be between 8-" + str(max_password_length) + " characters.")

        data = dict(email="valid@email.com", password="a" * (max_password_length + 1))
        tester(data, "Password must be between 8-" + str(max_password_length) + " characters.")

        data = dict(email="valid@email.com", password="notalphanumeric!@#$")
        tester(data, "Only alphanumeric characters are allowed in a password.")

        User.objects.all().delete()
        data = dict(email="test@gmail.com", password="testpassword")
        test_user = user_datastore.create_user(email=data['email'], password=data['password'])
        tester(data, "Email already in use, please use another one")
        user_datastore.delete_user(test_user)
    
        data = dict(email="new1Emai2lNo24bo5dyShouldHave@gmail.com", password="validPassword123")
        tester(data, "Account has been created! Check your email to validate your account.", correct_code=200, key="success")
        test_user = User.objects.get(email=data['email'])
        user_datastore.delete_user(test_user)

    def test_authenticate(self):
        valid_email = "validEmail@gmail.com"
        valid_password = "validPassword123"
        encrypted_password = bcrypt.hashpw(valid_password.encode(), bcrypt.gensalt())
        test_user = user_datastore.create_user(email=valid_email, password=encrypted_password)

        def tester(data, string, correct_code=422, key='error'):
            response, code = self.request('api/auth', data)
            assert code == correct_code
            assert response[key] == string
        
        #correct email and password
        data = dict(email=valid_email, password=valid_password)
        response, code = self.request('api/auth', data)
        assert code == 200
        assert response['email'] == valid_email
        assert test_user.verify_auth_token(response['auth_token'])
        
        #wrong password
        data['password'] = 'invalidPassword'
        tester(data, "Incorrect email or password")
        
        #wrong email
        data['email'] = 'invalid@email.com'
        data['password'] = valid_password
        tester(data, "Incorrect email or password")
        
        #wrong email and password
        data['email'] = 'invalid@email.com'
        data['password'] = 'invalidPassword'
        tester(data, "Incorrect email or password")

        user_datastore.delete_user(test_user)

    def test_create_map(self):
        valid_email = "validEmail@gmail.com"
        valid_password = "validPassword123"
        encrypted_password = bcrypt.hashpw(valid_password.encode(), bcrypt.gensalt())
        test_user = user_datastore.create_user(email=valid_email, password=encrypted_password)

        data = self.request('/api/auth', dict(email=valid_email, password=valid_password))[0]

        def tester(data, correct_code):
            request, code = self.request('/api/map', data)
            request_match = correct_code == code
            if not request_match: print("FAILURE, variables:", code, request)
            assert request_match
            return request

        # Malformed request (is missing the map)
        assert "Malformed request" == tester(data, 422)['error']

        # Bad token
        correct_auth_token = data['auth_token']
        data['map'] = "exists"
        data['auth_token'] = "garbage"
        assert "Invalid token" == tester(data, 401)['error']

        # Map in request, but missing the key 'color'
        data['auth_token'] = correct_auth_token
        map_dict = dict(width=4, height=5, depth=6, private=True, models=[])
        data['map'] = dumps(map_dict)
        assert "Malformed request" == tester(data, 422)['error']

        # Correct data scenario
        map_dict['color'] = "#fff"
        data['map'] = dumps(map_dict)
        map_and_success = tester(data, 200)

        assert map_and_success['success'] == "Successfully created map"

        map = map_and_success['map']
        for i in map_dict.keys():
            assert map_dict[i] == map[i]

        # TODO: make sure this line is safe; idk if the maps are actually being
        # used in the temp DB, it looks like they're actually in the dev DB.
        Map.delete(map)
        user_datastore.delete_user(test_user)

if __name__ == "__main__":
    unittest.main()        
