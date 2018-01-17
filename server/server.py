# Pip
from flask import Flask, render_template, request, url_for, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore, login_required
import bcrypt
from passlib.apps import custom_app_context as pwd_context
import re

# Our code
import secrets
from models import *

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = secrets.SECRET_KEY

# MongoDB Config
app.config['MONGODB_DB'] = 'mydatabase'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017

# CORS Config
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Email Config
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = secrets.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = secrets.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Create database connection object
db = MongoEngine(app)

# Define valid email, password patterns
email_pattern = re.compile('[\\w.]+@[\\w]+.[\\w]+', re.IGNORECASE)
max_email_length = 255
max_password_length = 255

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/protected')
@login_required
def protected():
	return 'This is a protected route.'

def send_email(text, recipients, subject="AR-top"):
	try:
		msg = Message(subject, sender="kruk@gmail.com", recipients = recipients)
		msg.body = text
		mail.send(msg)
	except Exception as e:
		app.logger.error("Failed to send message to " + str(recipients) + "\n" + str(e))
	
@app.route('/api/register', methods=['POST'])
def register():
	# Confirm the request
	email,password = None,None
	try:
		# TODO: switch this back to form in production
		# Postman doesn't always work for form. So for now lets use args.
		email = request.args["email"]
		password = request.args["password"]
	except:
		return jsonify(error="Malformed request; expecting email and password")
	
	# Validate the request
	if len(email) > max_email_length:
		return jsonify(error="Email can't be over " + str(max_email_length) + " characters.")
	if not email_pattern.match(email):
		return jsonify(error="Email not valid.")
	if len(password) < 8 or len(password) > max_password_length:
		return jsonify(error="Password must be between 8-" + str(max_password_length) + " characters.")
	if not str.isalnum(password):
		return jsonify(error="Only alphanumeric characters are allowed in a password.")
	
	# Try to retrieve a user object if it exists; 
	user = User.objects(email = email)
	if len(user) != 0:
		return jsonify(error="Email already in use, please use another one")
	
	# Hash and create user
	hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
	user_datastore.create_user(email=email, password=hashed)
	
	# TODO: error handle this and if it doesn't work do something else besides the success in jsonify
	#send_email(recipients=[email], subject="ay whaddup", text="Hello from AR-top")
	
	return jsonify(success="Account has been created! Check your email to validate your account.")

@app.route('/auth', methods=['POST'])
def authenticate():
	email, password = None, None
	try:
		# TODO: switch this back to form in production
		# Postman doesn't always work for form. So for now lets use args.
		email = request.args.get("email")
		password = request.args.get("password")
	except:
		return jsonify({"error": "Malformed Request; expecting email and password"}), 422, {'Content-Type': 'application/json'}

	error = None
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
	from argparse import ArgumentParser
	
	parser = ArgumentParser(description="Runs flask server")

	# TODO: logic not implemented for this because we should wait
	parser.add_argument("mode", nargs='?', choices=['d', 'p'], help="Selects whether or not you want to run development or production")
	parser.add_argument("-e", "--email", nargs='+', type=str, help="Sends an email if you use characters commandline can understand")
	parser.add_argument("-r", "--recipients", nargs='+', type=str, help="Who you want to send to")
	parser.add_argument("-u", "--user", nargs=2, type=str, help="Insert a new user: takes username, password")
	args = parser.parse_args()

	if args.email is not None:
		if args.recipients is None:
			print("You need to include recipients to email if you want to send an email.")
		else:
			send_email(text=' '.join(args.email), recipients=args.recipients)
		exit()

	app.run()
