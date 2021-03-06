import random
import secrets
import sys
from json import dumps, loads
from datetime import datetime as dt
from bson import ObjectId
from flask import current_app
from flask_security import (MongoEngineUserDatastore, RoleMixin, Security,
                            UserMixin, login_required)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from mongoengine import (BooleanField, DateTimeField, Document, DoesNotExist,
                         EmailField, EmbeddedDocument, EmbeddedDocumentField,
                         EmbeddedDocumentListField, IntField, ListField,
                         ObjectIdField, ReferenceField, StringField)

from constants import max_size, session_code_choices
from flask_socketio import SocketIO


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
    x = IntField(required=True, choices=range(0, max_size))
    y = IntField(required=True, choices=range(0, max_size))
    z = IntField(required=True, choices=range(0, max_size))


class GameModel(EmbeddedDocument):
    """ This schema should be used to represent any model that can be placed into a map.

    Keywoard arguments:
    EmbeddedDocument -- Representation of a One-To-Many Relationship.

    """
    type = StringField(required=True, choices=[
        'voxel',
        'floor',
        'wall',
        'fighter',
        'ranger',
        'knight',
        'goblin',
    ])
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
    models = EmbeddedDocumentListField(GameModel)
    updated = DateTimeField(default=dt.now())
    inserted = DateTimeField(default=dt.now())

    def save(self, *args, **kwargs):
        self.updated = dt.now()
        super(GameMap, self).save(*args, **kwargs)


class User(Document, UserMixin):
    """ Model for what fields a user can have in Mongo.

    Keyword arguments:
    Document -- The base class used for defining the structure and properties of collections of documents stored in MongoDB.
    UserMixin -- Mixin for User model definitions.

    """
    updated = DateTimeField(default=dt.now())
    inserted = DateTimeField(default=dt.now())
    email = EmailField(max_length=255, unique=True)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])
    verified = BooleanField(default=False)
    updated = DateTimeField(default=dt.now())
    inserted = DateTimeField(default=dt.now())

    def save(self, *args, **kwargs):
        self.updated = dt.now()
        super(User, self).save(*args, **kwargs)

    def verify_password(self, password):
        """ Verify password match """
        return password == self.password

    def generate_auth_token(self, expiration=86400):
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
            if not current_app.testing:
                current_app.logger.error(e)
            return None
        user = User.objects.get(email=data['id'])
        return user

#=====================================================
# Session model
#=====================================================


class Session(Document):
    """ Model for sessions.

    Keyword arguments:
    Model -- The base class for all in-house documents.

    """
    user_id = ObjectIdField()
    game_map_id = ObjectIdField()
    code = StringField(regex='^([A-Za-z0-9]{5})$',  unique=True)
    created_at = DateTimeField(default=dt.now())

    def save(self, *args, **kwargs):
        if self.code == None:
            code_try = ''
            for _ in range(0, 5):
                code_try += random.choice(session_code_choices)
            while len(Session.objects(code=code_try)) != 0:
                code_try = ''
                for _ in range(0, 5):
                    code_try += random.choice(session_code_choices)
            self.code = code_try

        game_map = GameMap.objects(id=self.game_map_id).first()
        game_map = game_map.to_json()
        game_map = loads(game_map)
        name = game_map["name"]
        color = game_map["color"]
        models = game_map["models"]
        depth = game_map["depth"]
        height = game_map["height"]
        width = game_map["width"]
        if current_app.config['REDIS_HOST'] is None or current_app.config['REDIS_HOST'] == "":
            socketio = SocketIO(message_queue='redis://')
        else:
            socketio = SocketIO(message_queue='redis://' +
                                current_app.config['REDIS_HOST'])
        socketio.emit(
            'update', {'name': name, 'color': color, 'models': models, 'depth': depth, 'width': width, 'height': height})
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        socketio = SocketIO(message_queue='redis://' + current_app.config['REDIS_HOST'])
        socketio.emit('close_room', self.code)
        
        super().save(*args, **kwargs)
