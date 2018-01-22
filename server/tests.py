import unittest
from server import *
import tempfile
from json import loads
import os

class TestRegistration(unittest.TestCase):
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
    def tester(data, string, correct_code=422, key='error'):
      response, code = self.request('api/auth', data)
      assert code == correct_code
      assert response[key] == string

    email = 'validEmail@gmail.com'
    password = 'validpassword123'.encode('utf-8')

    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    test_user = user_datastore.create_user(email=email, password=hashed)

    data = dict(email=email, password=password.decode('utf-8'))
    response, code = self.request('api/auth', data)
    assert code == 200
    assert response.get('auth_token') is not None
    assert response.get('email') == email
    
    data['password'] = 'invalidPassword'
    tester(data, "Incorrect email or password")

    data['email'] = 'invalid@email.com'
    tester(data, "Incorrect email or password")
    
    user_datastore.delete_user(test_user)
    
if __name__ == "__main__":
  unittest.main()        
