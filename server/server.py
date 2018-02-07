import secrets
from json import loads

from flask import Blueprint, Flask, jsonify, render_template, request, url_for
from flask_mail import Mail, Message
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security, login_required
from passlib.apps import custom_app_context as pwd_context

from api import *
from constants import internal_error, json_tag, malformed_request
from decorators import *
from flask_cors import CORS
from helper import *
from models import *

#=====================================================
# Constants
#=====================================================

#=====================================================
# App skeleton
#=====================================================
# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = secrets.SECRET_KEY

# MongoDB Config
app.config['MONGODB_DB'] = 'mydatabase'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017

# CORS Config
CORS(app, resources={r"/api/*": {"origins": "*"}},
     expose_headers=['Content-Type', 'Authorization'])

# Email Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = secrets.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = secrets.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Create database connection object
db = MongoEngine(app)

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create Blueprint
api = Blueprint("api", "api", url_prefix="/api")

#=====================================================
# Code for later in the project
#=====================================================


@app.route('/')
def index():
    return render_template('index.html')


def send_email(text, recipients, subject="AR-top"):
    if type(recipients) is str:
        recipients = [recipients]

    try:
        msg = Message(subject, sender=secrets.MAIL_USERNAME,
                      recipients=recipients)
        msg.body = text
        mail.send(msg)
    except Exception as e:
        app.logger.error("Failed to send message to " +
                         str(recipients) + "\n" + str(e))

#=====================================================
# User related routes
#=====================================================


@api.route('/register', methods=['POST'])
@protected
def register(claims):
    return Api.register(claims)


@api.route('/auth', methods=['POST'])
@protected
def authenticate(claims):
    return Api.authenticate(claims)

#=====================================================
# Map routes
#=====================================================


@api.route('/map/<id>', methods=['GET'])
@protected
def read_maps(claims, id):
    return Api.read_maps(claims, id)


@api.route("/maps/<string:user_id>", methods=['GET'])
@protected
def read_list_of_maps(claims, user_id):
    token = claims['auth_token']
    token_user = User.verify_auth_token(token)
    map_list = None
    if token_user is None:
        error = "token expired"
    # I am assuming that the user will need to login again and I don't need to check password here
    else:
        map_list = Map.objects(user=token_user)
        if map_list == None:
            error = "map error"
        else:
            return map_list.to_json(), 200, json_tag
    return jsonify(error=error), 422, json_tag


@api.route("/map", methods=["POST"])
@protected
def create_map(claims):
    email, map, user = None, None, None
    try:
        # Use a dict access here, not ".get". The access is better with the try block.
        email = claims["email"]
        user = User.objects(email=email).first()
        map = request.json['map']
    except Exception as e:
        if not app.testing:
            app.logger.error(str(e))
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
        app.logger.error(str(e))
        return malformed_request()

    try:
        new_map = Map(name=name, user=user, width=width, height=height, depth=depth,
                      color=color, private=private, models=models)
        new_map.save()
    except Exception as e:
        app.logger.error("Failed to save map for user",
                         str(user), "\n", str(e))
        return internal_error()

    return jsonify(success="Successfully created map", map=new_map), 200, json_tag


@api.route('/map/<map_id>', methods=['POST'])
@protected
def update_map(claims, map_id):
    try:
        # Use a dict access here, not ".get". The access is better with the try block.
        email = claims["email"]
        map = request.json['map']
        user = User.objects(email=email).first()
    except:
        return malformed_request()

    # Make sure this user is actually the author of the map
    # and that the ID also is an existing map
    remote_copy = None
    try:
        remote_copy = Map.objects.get(id=map_id, user=user)
    except (StopIteration, DoesNotExist) as e:
        # Malicious user may be trying to overwrite someone's map
        # or there actually is something wrong; treat these situations the same
        return jsonify(error="Map does not exist"), 404, json_tag
    except Exception as e:
        app.logger.error(str(e))
        return internal_error()

    try:
        for i in ["name", "width", "height", "depth", "color", "private", 'models']:
            attr = map.get(i)
            if attr:
                remote_copy[i] = attr
    except:
        return internal_error()

    return jsonify(success="Map updated successfully", map=remote_copy), 200, json_tag


@api.route('/map/<map_id>', methods=['DELETE'])
@protected
def delete_map(claims, map_id):
    email = None
    try:
        email = claims["email"]
    except:
        return malformed_request()

    try:
        user = User.objects(email=email).first()
    except:
        return internal_error()

    try:
        remote_copy = Map.objects.get(id=map_id, user=user)
        remote_copy.delete()
    except (StopIteration, DoesNotExist) as e:
        # Malicious user may be trying to overwrite someone's map
        # or there actually is something wrong; treat these situations the same
        return jsonify(error="Map does not exist"), 404, json_tag
    except:
        return internal_error()

    return jsonify(success=map_id), 200, json_tag


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
