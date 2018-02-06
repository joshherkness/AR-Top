import os
import secrets
import tempfile
import unittest
from json import dumps, loads

import bcrypt
from server import *


class TestUserEndpoints(unittest.TestCase):
    #=====================================================
    # Skeleton (you can fold this code)
    #=====================================================
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()
  
    def tearDown(self):
        Map.objects.all().delete()
        User.objects.all().delete()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    #=====================================================
    # Helper methods
    #=====================================================
    def request(self, page, data=None, method='POST'):
        headers = {
                'Authorization': 'Bearer ' + jwt.encode(dict(data=data), base64.b64decode(secrets.JWT_KEY), algorithm='HS512').decode()
        }

        response = self.app.open(page, method=method, data=data, follow_redirects=True, headers=headers)
        json = loads(response.data.decode('utf-8'))
        return json, response.status_code

    #=====================================================
    # Tests
    #=====================================================
    def test_register(self):
        def tester(data, string, correct_code=422, key='error'):
            response, code = self.request('api/register', data)
            self.assertEqual(code, correct_code)
            self.assertEqual(string, response[key])

        data = dict(email="malformed", passwd="request")
        tester(data, "Malformed request")

        data = dict(email="a" * (max_email_length + 1), password="email too long")
        tester(data, "Email can't be over " + str(max_email_length) + " characters.")

        for i in ["bad email1", "badEmail@2", ""]:
            data = dict(email=i, password="something")
            tester(data, "Email not valid.")

        data = dict(email="valid@email.com", password="tooshrt")
        tester(data, "Password must be between 8-" + str(max_password_length) + " characters.")

        data = dict(email="valid@email.com", password="a" * (max_password_length + 1))
        tester(data, "Password must be between 8-" + str(max_password_length) + " characters.")

        data = dict(email="valid@email.com", password="notalphanumeric_")
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

        def tester(data, correct_code, key, string):
            request, code = self.request('/api/map', data)
            self.assertEqual(correct_code, code)
            self.assertEqual(string, request[key])
            return request

        # Malformed request (is missing the map)
        tester(data, 422, 'error', "Malformed request")

        # Bad token
        correct_auth_token = data['auth_token']
        data['map'] = dumps({})
        data['auth_token'] = "garbage"
        tester(string="Invalid token", data=data, correct_code=401, key='error')

        # Map in request, but missing the key 'color'
        data['auth_token'] = correct_auth_token
        map_dict = dict(width=4, height=5, depth=6, private=True, models=[])
        data['map'] = dumps(map_dict)
        tester(string="Malformed request",data=data, correct_code=422, key='error')

        # Correct data scenario
        map_dict['color'] = "#fff"
        data['map'] = dumps(map_dict)
        map = tester(data=data, correct_code=200, key='success', string="Successfully created map")

        map = map_and_success['map']
        for i in map_dict.keys():
            self.assertEqual(map_dict[i], map[i])

        # TODO: make sure this line is safe; idk if the maps are actually being
        # used in the temp DB, it looks like they're actually in the dev DB.
        # Map.delete(map)
        user_datastore.delete_user(test_user)

    def test_read_map(self):
        valid_email = "validEmail@gmail.com"
        valid_password = "validPassword123"
        encrypted_password = bcrypt.hashpw(valid_password.encode(), bcrypt.gensalt())
        test_user = user_datastore.create_user(email=valid_email, password=encrypted_password)
        
        valid_email2 = "tests2@gmail.com"
        valid_password2 = "testPassword2"
        encrypted_password2 = bcrypt.hashpw(valid_password2.encode(), bcrypt.gensalt())
        test_user2 = user_datastore.create_user(email=valid_email2, password=encrypted_password2)
        
        api_token1 = self.request('/api/auth', dict(email=valid_email, password=valid_password))[0]
        api_token2 = self.request('/api/auth', dict(email=valid_email2, password=valid_password2))[0]
        
        def tester(data, string, id, correct_code=422, key="error"):
            response, code = self.request('/api/map/' + str(id), data, method='GET')
            assert code == correct_code
            return response
        try:
            test_map = Map(user=test_user, color="#FFFFFF", private=True, )
            test_map.save()
            test_id = test_map.id
            
            # User reading map that they are the Owner of
            result_map = tester(data, "", test_id, correct_code=200)
            assert result_map['user']['$oid'] == test_user.get_id()
            
            # Map in response has the id that was requested
            assert result_map['_id']['$oid'] == str(test_id)
            
            # User reading map that they are not the Owner of
            result_string = tester(data2, "map error", test_id, correct_code=422)['error']
            assert result_string == "map error"
        
        finally:
            test_map.delete()
            user_datastore.delete_user(test_user)
            user_datastore.delete_user(test_user2)

    def test_read_list_of_maps(self):
        valid_email = "validEmail@gmail.com"
        valid_password = "validPassword123"
        encrypted_password = bcrypt.hashpw(valid_password.encode(), bcrypt.gensalt())
        test_user = user_datastore.create_user(email=valid_email, password=encrypted_password)
        test_user_id = test_user.id
        auth_token = self.request('/api/auth', dict(email=valid_email, password=valid_password))[0]
        auth_token = dict(auth_token=auth_token['auth_token'])

        def tester(data, string, id, correct_code=422, key="error"):
            response, code = self.request('/api/maps/' + str(id), data, method='GET')
            assert code == correct_code
            return response

        tester(auth_token, "", test_user_id, correct_code=200)

    def test_update_map(self):
        pass
        
if __name__ == "__main__":
    unittest.main()        
