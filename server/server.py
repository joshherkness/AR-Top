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
    if request.method == 'POST':
        app.logger.debug("" + request.args.get('email'))
        if valid_login(request.args.get('email'), 
                      request.args.get('password')):
            auth_token = '123456'
            return jsonify({'email': request.args.get('email'), 'auth_token': auth_token}), 200, {'Content-Type': 'application/json'} #return username and auth token
        else:
            return jsonify({'error': "Incorrect email or password"}), 422, {'Content-Type': 'application/json'}


    #if successful
    #if not

def valid_login(email, password):
    return False

if __name__ == '__main__':
    app.run()
