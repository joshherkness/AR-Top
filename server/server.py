from flask import Flask, render_template, request, jsonify
from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as
     Serializer, BadSignature, SignatureExpired)
import re

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

# Define valid email, password patterns
email_pattern = re.compile('[\\w.]+@[\\w]+.[\\w]+', re.IGNORECASE)
max_email_length = 255
max_password_length = 255

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=max_email_length)
    password = db.StringField(max_length=max_password_length)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    def verify_password(self, password):
        return password == self.password

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.email })

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
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.objects(email = email)
    if len(user) < 1:
        error = "Incorrect email or password"
        return jsonify({'error': error}), 422, {'Content-Type': 'application/json'}
    if request.method == 'POST':
        if valid_login(email, password) and user[0].verify_password(password):
            auth_token = user[0].generate_auth_token()
            return jsonify({'email': request.form.get('email'), 'auth_token': auth_token}), 200, {'Content-Type': 'application/json'} #return username and auth token
        else:
            error = "Incorrect email or password"
    else:
        error = "Incorrect email or password"
    return jsonify({'error': error}), 422, {'Content-Type': 'application/json'}

def valid_login(email, password):
    if email_pattern.match(email.encode('utf-8')) and len(email.encode('utf-8')) <= max_email_length:
        if str.isalnum(password.encode('utf-8')) and len(password.encode('utf-8')) <= max_password_length:
            return True
    return False        

if __name__ == '__main__':
    app.run()