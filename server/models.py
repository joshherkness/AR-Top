import secrets
import sys
from datetime import datetime

from bson import ObjectId
from flask_security import (MongoEngineUserDatastore, RoleMixin, Security,
                            UserMixin, login_required)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from mongoengine import *
from mongoengine.fields import *

from constants import max_size


class Role(Document, RoleMixin):
    """ Model for what roles a user can have.

    Keyword arguments:
    Document -- The base class used for defining the structure and properties of collections of documents stored in MongoDB.
    RoleMixin -- Mixin for Role model definitions.

    """
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)


class Position(EmbeddedDocument):
    """ This schema should be used to represent a three dimensional position using x, y, and z integer coordinates.

    Keywoard arguments:
    EmbeddedDocument -- Representation of a One-To-Many Relationship.

    TODO: Make this more modular, and independent of max_size
    """
    x = IntField(required=True, choices=range(1, max_size + 1))
    y = IntField(required=True, choices=range(1, max_size + 1))
    z = IntField(required=True, choices=range(1, max_size + 1))


class Voxel(EmbeddedDocument):
    """ This schema should be used to represent any model that can be placed into a map.

    Keywoard arguments:
    EmbeddedDocument -- Representation of a One-To-Many Relationship.

    """
    type = StringField(required=True, choices=['voxel'])
    position = EmbeddedDocumentField(Position)
    color = StringField(
        required=True, regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')


class GameMap(Document):
    """ Model for what fields a map can have in Mongo.

    Keyword arguments:
    EmbeddedDocument -- Representation of a One-To-Many Relationship.

    """
    owner = ObjectIdField()
    name = StringField(max_length=255)
    width = IntField(default=16, choices=range(1, max_size + 1))
    height = IntField(default=5, choices=range(1, max_size + 1))
    depth = IntField(default=16, choices=range(1, max_size + 1))
    color = StringField(
        required=True, regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    private = BooleanField(default=False)
    voxels = EmbeddedDocumentListField(Voxel)
    updated = DateTimeField(default=datetime.now())
    inserted = DateTimeField(default=datetime.now())


class User(Document, UserMixin):
    """ Model for what fields a user can have in Mongo.

    Keyword arguments:
    Document -- The base class used for defining the structure and properties of collections of documents stored in MongoDB.
    UserMixin -- Mixin for User model definitions.

    """
    updated = DateTimeField(default=datetime.now())
    inserted = DateTimeField(default=datetime.now())
    email = EmailField(max_length=255, unique=True)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])
    verified = BooleanField(default=False)
    updated = DateTimeField(default=datetime.now())
    inserted = DateTimeField(default=datetime.now())

    def verify_password(self, password):
        """ Verify password match """
        return password == self.password

    def generate_auth_token(self, expiration=600):
        """ Generate a JWS token for the user. """
        s = Serializer(secrets.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.email})

    @staticmethod
    def verify_auth_token(token):
        """ Verify token is still valid for user. """
        s = Serializer(secrets.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        except Exception as e:
            print("ERROR IN User.verify_auth_token function")
            return None
        user = User.objects.get(email=data['id'])
        return user
