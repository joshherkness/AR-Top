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

#=====================================================
# Superclasses
#=====================================================
class Model(Document):
    updated = DateTimeField(default=datetime.now())
    inserted = DateTimeField(default=datetime.now())
    meta = {'allow_inheritance': True}
  
    def save(self, *args, **kwargs):
        updated = datetime.now()
        super().save(*args, **kwargs)

#=====================================================
# User related models
#=====================================================
class Role(Document, RoleMixin):
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
        user = User.objects.get(email=data['id'])
        return user

#=====================================================
# Map models
#=====================================================
class Position(EmbeddedDocument):
    """
    This schema should be used to represent a three dimensional
    position using x, y, and z integer coordinates.

    TODO: Make this more modular, and independent of max_size
    """
    x = IntField(required=True, choices=range(1,max_size + 1))
    y = IntField(required=True, choices=range(1,max_size + 1))
    z = IntField(required=True, choices=range(1,max_size + 1))

class RGBColor(EmbeddedDocument):
    """
    This schema should be used to represent an rgb color, where
    each rgb value must be within a normalized range of 0 to 1.

    TODO: Don't know if we want to use this vs. hex value, but
    it is created just in case.
    """
    r = DecimalField(required=True, min_value=0, max_value=1, precision=3)
    g = DecimalField(required=True, min_value=0, max_value=1, precision=3)
    b = DecimalField(required=True, min_value=0, max_value=1, precision=3)

class MapModel(EmbeddedDocument):
    """
    This schema should be used to represent any model that can be
    placed into a map.
    """
    type = StringField(required=True, choices=['voxel'])
    position = EmbeddedDocumentField(Position)
    color = StringField(required=True, regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')

class Map(Model):
    user = ReferenceField(User) # this means foreign key
    width = IntField(default=16, choices=range(1,max_size + 1))
    height = IntField(default=5, choices=range(1,max_size + 1))
    depth = IntField(default=16, choices=range(1,max_size + 1))
    color = StringField(required=True, regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    private = BooleanField(default=False)
    models = EmbeddedDocumentListField(MapModel)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # TODO: socket.io or whatever the hell it is
