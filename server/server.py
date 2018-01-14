import re
from flask import Flask, render_template, request, jsonify
from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'

# MongoDB Config
app.config['MONGODB_DB'] = 'mydatabase'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017

# Create database connection object
db = MongoEngine(app)

# Define valid email pattern
email_pattern = re.compile('[\\w.]+@[\\w]+.[\\w]+', re.IGNORECASE)
max_email_length = 254

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.create_user(email='mercer@exandria.net', password='password')

# Routes
@app.route('/')
def index(): return render_template('index.html')

@app.route('/protected')
@login_required
def protected():
    return 'This is a protected route.'

@app.route('/auth', methods=['POST'])
def authenticate():
    error = None
    email = request.args.get('email')
    password = request.args.get('password')
    if request.method == 'POST' and str.isalnum(password.encode('utf-8')) and is_valid_email_address(email.encode('utf-8')):
        if valid_login(email, password):
            auth_token = '123456' #TODO
            return jsonify({'email': request.args.get('email'), 'auth_token': auth_token}), 200, {'Content-Type': 'application/json'} #return username and auth token
        else:
            error = "Incorrect email or password"
    else:
        error = "Incorrect email or password"
    return jsonify({'error': error}), 422, {'Content-Type': 'application/json'}



    #if successful
    #if not

def valid_login(email, password):
    return True

def is_valid_email_address(email=""):
    if email_pattern.match(email) and len(email) <= max_email_length:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run()
