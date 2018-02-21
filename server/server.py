import secrets
from json import loads

from flask import Blueprint, Flask, jsonify, render_template, request, url_for
from flask_mongoengine import MongoEngine

from api import *
from constants import internal_error, json_tag, malformed_request
from decorators import *
from flask_cors import CORS
from helper import *
from models import *

# Create app
app = Flask(__name__)

# Load configuration from config file.
app.config.from_object('config')

# Set CORS
CORS(app, resources={r"/api/*": {"origins": "*"}},
     expose_headers=['Content-Type', 'Authorization'])

# Setup DB connection.
db = MongoEngine(app)

# Instantiate Api to use DB Connection for user_datastore.
# To remove circular dependency.
Api(db)

# Create Blueprint
api = Blueprint("api", "api", url_prefix="/api")

# IS THIS BEING USED???
# Setup Flask-Security
# security = Security(app, user_datastore)


@app.route('/')
def index():
    """ Entry point to site for production. """
    return render_template('index.html')


#=====================================================
# User related routes
#=====================================================

@api.route('/register', methods=['POST'])
@protected
def register(claims):
    """ Register user with credentials in claims. """
    # This is to remove the circular dependency.
    api = Api(db)
    return api.register(claims)


@api.route('/auth', methods=['POST'])
@protected
def authenticate(claims):
    """ Log user in with credentials in claims. """
    return Api.authenticate(claims)

@api.route('/authenticated', methods=['GET'])
@protected
@expiration_check
def authenticated(claims, token_user):
    return jsonify(user=token_user), 200, json_tag

#=====================================================
# Map routes
#=====================================================


@api.route('/map/<id>', methods=['GET'])
@protected
def read_map(claims, id):
    """ Return a single map by id. """
    return Api.read_map(claims, id)


@api.route("/maps/<string:user_id>", methods=['GET'])
@protected
def read_list_of_maps(claims, user_id):
    """ Get all maps for a user. """
    return Api.read_list_of_maps(claims, user_id)


@api.route("/map", methods=["POST"])
@protected
def create_map(claims):
    """ Creates a map. """
    return Api.create_map(claims)


@api.route('/map/<map_id>', methods=['POST'])
@protected
def update_map(claims, map_id):
    """ Updates a maps name or color by id. """
    return Api.update_map(claims, map_id)


@api.route('/map/<map_id>', methods=['DELETE'])
@protected
def delete_map(claims, map_id):
    """ Deletes a specified map by id. """
    return Api.delete_map(claims, map_id)

@api.route('/sessions/', methods=['POST'])
@protected
@expiration_check
def create_session(claims, token_user):
    """ Creates a session with the given map_id and token user's id """
    return Api.create_session(claims,token_user)


#=====================================================
# Main
#=====================================================
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Runs flask server")

    # TODO: logic not implemented for this because we should wait
    parser.add_argument("mode", nargs='?', choices=[
                        'd', 'p'], help="Selects whether or not you want to run development or production")
    parser.add_argument("-e", "--email", nargs='+', type=str,
                        help="Sends an email if you use characters commandline can understand")
    parser.add_argument("-r", "--recipients", nargs='+',
                        type=str, help="Who you want to send to")
    parser.add_argument("-u", "--user", nargs=2, type=str,
                        help="Insert a new user: takes username, password")
    args = parser.parse_args()
    if args.email is not None:
        if args.recipients is None:
            print("You need to include recipients to email if you want to send an email.")
        else:
            send_email(text=' '.join(args.email), recipients=args.recipients)
        exit()
    app.register_blueprint(api)
    app.run()

GameMap.drop_collection()
