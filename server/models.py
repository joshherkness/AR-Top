import secrets

from flask_security import (MongoEngineUserDatastore, RoleMixin, Security,
                            UserMixin, login_required)

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

from mongoengine import *
from mongoengine.fields import *

from datetime import datetime

import sys

max_size = 1024

# All models inherit from this. It contains the fields we
# need for important data
class Model(Document):
    updated = DateTimeField(default=datetime.now())
    inserted = DateTimeField(default=datetime.now())
    
    meta = {'allow_inheritance': True}
  
    def save(self, *args, **kwargs):
        updated = datetime.now()
        super().save(*args, **kwargs)


# Maybe this could come in handy
class Voxel(BaseField):
    color = BinaryField()
    x = IntField(required=True, choices=range(1,max_size + 1))
    y = IntField(required=True, choices=range(1,max_size + 1))
    z = IntField(required=True, choices=range(1,max_size + 1))

class Map(Model):
    width = IntField(default=16, choices=range(1,max_size + 1))
    height = IntField(default=5, choices=range(1,max_size + 1))
    depth = IntField(default=16, choices=range(1,max_size + 1))
    base_color = BinaryField()
    private = BooleanField(default=False)
    models = ListField() #default is [], meaning empty map
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # TODO: socket.io or whatever the hell it is
        
class Role(Model, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)

class User(Model, UserMixin):
    email = EmailField(max_length=255)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])
    verified = BooleanField(default=False)
  
    def verify_password(self, password):
        return password == self.password
  
    def generate_auth_token(self, expiration=600):
        s = Serializer(secrets.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.email})
  
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secrets.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user
