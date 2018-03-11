import sys
import traceback
from json import loads
from datetime import datetime

from flask import current_app, jsonify, request
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security

from helper import Helper
from constants import json_tag, malformed_request, internal_error

from models import GameMap, User, Role, Session
from flask_socketio import SocketIO
from mongoengine import DoesNotExist


class Api():
    def __init__(self, db):
        """Init function for Api class.

        Keyword arguments:
        db -- The DB connection for the Flask app.

        Sets the instance variable.
        """
        self.user_datastore = MongoEngineUserDatastore(db, User, Role)

    def register(self, claims):
        """Register a new account in system

        Keyword arguments:
        claims -- The JWT claims that are being passed to this methods. Must include email and password for successful creation.

        Returns a HTTP response.
        """
        email, password = None, None
        try:
            if claims is not None:
                # Use a dict access here, not ".get". The access is better with the try block.
                email = str(claims['email'])
                password = str(claims['password'])
            else:
                return jsonify(error="Forbidden"), 403, json_tag
        except Exception as e:
            current_app.logger.error(e)
            if not current_app.testing:
                current_app.logger.error(e)
            return malformed_request()

        validation = Helper.validate_register(email, password)
        if validation[0] is True:
            return jsonify(error=validation[1]), 422, json_tag

        # Hash and create user
        self.user_datastore.create_user(
            email=email, password=Helper.hashpw(password))

        # So we can log user in automatically after registration
        token = User.objects(email=email).first().generate_auth_token()

        # TODO: error handle this and if it doesn't work do something else besides the success in jsonify
        # send_email(recipients=email, subject="ay whaddup", text="Hello from AR-top")
        return jsonify(success="Account has been created! Check your email to validate your account.", auth_token=token.decode('utf-8')), 200, json_tag

    @staticmethod
    def authenticate(claims):
        """Verify a login attempt.

        Keyword arguments:
        claims -- The JWT claims that are being passed to this methods. Must include email and password for successful login.

        Returns a HTTP response.
        """
        email, password = None, None
        try:
            # Use a dict access here, not ".get". The access is better with the try block.
            if claims is not None:
                email = claims['email']
                password = claims["password"]
            else:
                return jsonify(error="Forbidden"), 403, json_tag
        except Exception as e:
            current_app.logger.error(str(e))
            return jsonify(error="Malformed Request; expecting email and password"), 422, json_tag

        validator = Helper.validate_auth(email, password)

        if validator[0] is True:
            return jsonify(error=validator[1]), 422, json_tag
        else:
            return jsonify(email=email, auth_token=validator[2]), 200, json_tag

    @staticmethod
    def read_map(claims, token_user, id):
        """Gather all maps associated with a user.

        Keyword arguments:
        claims -- The JWT claims that are being passed to this methods. Must include email.
        id -- The ID that is associated with the requested map.

        Returns a HTTP response.
        """
        game_map = None

        try:
            game_map = GameMap.objects(id=id, owner=token_user.id).first()
        except (StopIteration, DoesNotExist):
            current_app.logger.error(e)
            # Malicious user may be trying to overwrite someone's map
            # or there actually is something wrong; treat these situations the same
            return jsonify(error="Map does not exist"), 404, json_tag
        except Exception as e:
            current_app.logger.error(e)
            return internal_error()

        return jsonify(game_map), 200, json_tag

    @staticmethod
    def read_list_of_maps(claims, token_user, user_id):
        """Gather all maps associated with a user.

        Keyword arguments:
        claims -- The JWT claims that are being passed to this methods. Must include email.
        id -- The ID that is associated with the requested map.

        Returns a HTTP response.
        """
        map_list = None
        if token_user is None:
            error = "token expired"
        # I am assuming that the user will need to login again and I don't need to check password here
        else:
            map_list = GameMap.objects.exclude(
                'models').filter(owner=token_user.id)
            if map_list == None:
                error = "map error"
            else:
                return jsonify(map_list), 200, json_tag
        return jsonify(error=error), 422, json_tag

    @staticmethod
    def create_map(claims, token_user):
        """Create a map for the user.

        Keyword arguments:
        claims -- The JWT claims that are being passed to this methods. Must include email.

        Returns a HTTP response.
        """
        map = None
        try:
            # Use a dict access here, not ".get". The access is better with the try block.
            map = request.json['map']

            # The test send map as a string.
            if type(map) is not dict:
                map = loads(map)

        except Exception as e:
            if not current_app.testing:
                current_app.logger.error(str(e))
            return malformed_request()

        try:
            name = map["name"]
            width = map["width"]
            height = map["height"]
            depth = map["depth"]
            color = map["color"]
            private = map["private"]
            models = map['models']
        except Exception as e:
            current_app.logger.error(str(e))
            return malformed_request()

        try:
            new_game_map = GameMap(owner=token_user.id, name=name, width=width, height=height,
                                   depth=depth, color=color, private=private, models=models)
            new_game_map.save()
        except Exception as e:
            current_app.logger.error("Failed to save map for user",
                                     str(token_user), "\n", str(e))
            return internal_error()

        return jsonify(success="Successfully created map", map=new_game_map), 200, json_tag

    @staticmethod
    def update_map(claims, token_user, map_id):
        """Update a map.

        Keyword arguments:
        claims -- The JWT claims that are being passed to this methods. Must include email.
        map_id -- The ID that is associated with the requested map.

        Returns a HTTP response.
        """
        try:
            # Use a dict access here, not ".get". The access is better with the try block.
            map = request.json['map']
        except Exception as e:
            current_app.logger.error(str(e))
            return malformed_request()

        # Make sure this user is actually the author of the map
        # and that the ID also is an existing map
        remote_copy = None
        try:
            remote_copy = GameMap.objects(id=map_id, owner=token_user.id).first()
        except (StopIteration, DoesNotExist) as e:
            # Malicious user may be trying to overwrite someone's map
            # or there actually is something wrong; treat these situations the same
            return jsonify(error="Map does not exist"), 404, json_tag
        except Exception as e:
            current_app.logger.error(str(e))
            return internal_error()

        try:
            remote_copy.update(**map)
            game_map = GameMap.objects(id=map_id).first()
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
                'update', {'name': name, 'color': color, 'models': models, 'height': height, 'width': width, 'depth': depth})
            return jsonify(success="Map updated successfully", map=GameMap.objects(id=map_id).first()), 200, json_tag
        except AttributeError as e:
            # happens when remote copy is None
            return jsonify(error="Map does not exist"), 404, json_tag
        except Exception as e:
            current_app.logger.error(str(e))
            return internal_error()

    @staticmethod
    def delete_map(claims, token_user, map_id):
        """Delete map from database.

        Keyword arguments:
        claims -- The JWT claims that are being passed to this methods. Must include email.
        map_id -- The ID that is associated with the requested map.

        Returns a HTTP response.
        """
        try:
            remote_copy = GameMap.objects(id=map_id, owner=token_user.id).first()
            if remote_copy is None:
                return jsonify(error="Map does not exist"), 404, json_tag
            remote_copy.delete()
        except (StopIteration, DoesNotExist):
            # Malicious user may be trying to overwrite someone's map
            # or there actually is something wrong; treat these situations the same
            return jsonify(error="Map does not exist"), 404, json_tag
        except:
            return internal_error()
        return jsonify(success=map_id), 200, json_tag

    @staticmethod
    def create_session(claims, token_user):
        """Create session and save to database.

        Keyword arguments:
        claims -- The JWT claims that are being passed to this methods. Must include email.
        token_user -- the user of the token sent in the JWT header, provided by @expiration_check
        """
        map_id = None
        try:
            map_id = request.json['map_id']
        except:
            return malformed_request()

        # Make sure this user is actually the author of the map with map_id
        # and that the map_id is of an existing map
        try:
            game_map = GameMap.objects(
                id=map_id, owner=token_user.id).first()
            if game_map is None:
                return jsonify(error="Map does not exist"), 404, json_tag
        except (StopIteration, DoesNotExist) as e:
            # Malicious user may be trying to overwrite someone's map
            # or there actually is something wrong; treat these situations the same
            return jsonify(error="Map does not exist"), 404, json_tag
        except Exception as e:
            current_app.logger.error(str(e))
            return internal_error()

        try:
            new_session = Session(user_id=token_user.id,
                                  game_map_id=game_map.id)
            new_session.save()
        except Exception as e:
            current_app.logger.error("Failed to save session for user",
                                     str(token_user), "and map ", str(map_id), str(e))
            return internal_error()
        return jsonify(success="Successfully created session", session=new_session), 200, json_tag

    @staticmethod
    def delete_session(claims, token_user, session_id):
        """Create session and save to database.

        Keyword arguments:
        claims -- The JWT claims that are being passed to this methods. Must include token.
        token_user -- User object.

        Returns HTTP Response
        """
        try:
            session = Session.objects(
                id=session_id, user_id=token_user.id).first()
            session.delete()
        except Exception as e:
            current_app.logger.error(e)
            return internal_error()
        return jsonify(success="Successfully removed session"), 200, json_tag

    @staticmethod
    def update_session(claims, token_user, id):
        """ Updates an existing session with a new map id

        Keyword arguments:
        claims -- The JWT claims that are being passed to this methods. Must include email.
        token_user -- the user of the token sent in the JWT header, provided by @expiration_check
        id -- the id of the session to be updated
        map_id -- the map id to update the session with
        """
        map_id = None
        try:
            map_id = request.json['map_id']
        except:
            return malformed_request()

        # Make sure the map is owned by the token user
        game_map = None
        try:
            game_map = GameMap.objects(id=map_id, owner=token_user.id).first()
        except:
            return jsonify(error="Game map does not exist"), 404, json_tag

        try:
            session_entity = Session.objects(id=id).first()
            session_entity.game_map_id = game_map.id
            session_entity.save()
        except (StopIteration, DoesNotExist) as e:
            return jsonify(error="Session does not exist"), 404, json_tag
        except Exception as e:
            current_app.logger.error(str(e))
            return internal_error()

        return jsonify(success="Successfully updated session with new map", session=session_entity)

    @staticmethod
    def read_session(claims, token_user, id):
        """ Returns the session with the given id """

        # Make sure the session exists
        try:
            remote_copy = Session.objects(id=id).first()
        except (StopIteration, DoesNotExist) as e:
            return jsonify(error="Session does not exist"), 404, json_tag
        except Exception as e:
            current_app.logger.error(str(e))
            return internal_error()

        return jsonify(success="Successfully read session", session=remote_copy), 200, json_tag

    def read_session_user_id(claims, token_user):
        """ Read a session with given user_id """
        try:
            session_entity = Session.objects(user_id=token_user.id).first()
        except (StopIteration, DoesNotExist) as e:
            return jsonify(error="Session does not exist"), 404, json_tag
        except Exception as e:
            current_app.logger.error(str(e))
            return internal_error()

        if session_entity == None:
            return jsonify(error="Session does not exist"), 404, json_tag

        return jsonify(success="Successfully read session", session=session_entity), 200, json_tag
