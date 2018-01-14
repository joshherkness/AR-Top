from flask import Flask, render_template, request, url_for
from flask_mongoengine import MongoEngine
from flask import request, jsonify
from flask_cors import CORS
from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required
from secrets import SECRET_KEY

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = SECRET_KEY

# MongoDB Config
app.config['MONGODB_DB'] = 'mydatabase'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017
CORS(app, resources={r"/api/*": {"origins": "*"}})

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

@app.route('/register', methods=["GET", "POST"])
def register():
	try:
		if request.method == "POST":
			email = request.form['email']
			
		else:
			return {"error":""}
	except KeyError:
		return {"error": "Malformed request"}
	except Exception as e:
		return {"error": "Something went wrong"

@app.route('/protected')
@login_required
def protected():
    return 'This is a protected route.'

@app.route('/api/register', methods=['POST'])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    return jsonify("")

if __name__ == '__main__':
    app.run()
