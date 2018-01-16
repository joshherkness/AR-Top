from mongoengine import *
from flask_security import Security, MongoEngineUserDatastore, UserMixin, RoleMixin, login_required
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class Role(Document, RoleMixin):
	name = StringField(max_length=80, unique=True)
	description = StringField(max_length=255)

class User(Document, UserMixin):
	email = StringField(max_length=255)
	password = StringField(max_length=255)
	active = BooleanField(default=True)
	confirmed_at = DateTimeField()
	roles = ListField(ReferenceField(Role), default=[])
	verified = BooleanField(default=False)

	def verify_password(self, password):
		return password == self.password
		
	def generate_auth_token(self, expiration = 600):
		s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({'id': self.email})
	
	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token
		user = User.query.get(data['id'])
		return user
