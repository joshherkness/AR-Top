import unittest
from server import *

class TestRegistration(unittest.TestCase):
	# This function gets called to make a temp DB in sqlite for testing
	def setUp(self):
		self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
		app.config['DATABASE'] = tempfile.mkstemp()
		app.testing = True
		self.app = app.test_client()

	# This function gets called to do teardown
	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(flaskr.app.config['DATABASE'])
	
	def test_register(self):
		

if __name__ == "__main__":
	unittest.main()
