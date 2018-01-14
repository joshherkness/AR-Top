from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask import request, jsonify
from flask_cors import CORS
from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask_mail import Mail, Message
import bcrypt

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'

# MongoDB Config
app.config['MONGODB_DB'] = 'mydatabase'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017

# CORS Config
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Email Config
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

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
    verified = db.BooleanField(default=False)

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
#@app.before_first_request
#def create_user():
#    user_datastore.create_user(email='mercer@exandria.net', password='password')

# Routes
@app.route('/')
def index(): return render_template('index.html')

@app.route('/protected')
@login_required
def protected():
    return 'This is a protected route.'

@app.route('/api/register', methods=['POST'])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    hashed = ""
    if len(password) <= 7:
        return jsonify(error="Password does not satisfy minimum length")
    else:
        user = User.objects(email = email)
        if len(user) == 1:
            return jsonify(error="Email already in use")
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user_datastore.create_user(email=email, password=hashed)
        msg = Message('Hello', sender='', recipients = [email])
        msg.body = "Hello Flask message sent from Flask-Mail"
        mail.send(msg)

    return jsonify(success="Account has been created!")

if __name__ == '__main__':
    app.run()
