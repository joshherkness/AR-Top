import unittest
from server import *
import tempfile
from json import loads
import os
import bcrypt

class TestRegistration(unittest.TestCase):
  #=====================================================
  # Skeleton (you can fold this code)
  #=====================================================
  def setUp(self):
    self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['DATABASE'] = tempfile.mkstemp()
    app.testing = True
    self.app = app.test_client()
    
  
  def tearDown(self):
    os.close(self.db_fd)
    os.unlink(app.config['DATABASE'][1])

  #=====================================================
  # Helper methods
  #=====================================================
  def request(self, page, data):
    response = self.app.post(page, data=data, follow_redirects=True)
    print("**", response)
    json = loads(response.data.decode('utf-8'))
    return json, response.status_code

  #=====================================================
  # Tests
  #=====================================================

  def test_authenticate(self):
    def tester(data, string, correct_code=422, key='error'):
      response, code = self.request('api/auth', data)
      assert code == correct_code
      assert response[key] == string

    valid_email = 'validEmail@gmail.com'
    valid_password = 'validpassword123'
    encrypted_password = bcrypt.hashpw(valid_password.encode(), bcrypt.gensalt())
    
    test_user = user_datastore.create_user(email=valid_email, password=encrypted_password)

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
    
if __name__ == "__main__":
  unittest.main()        
