try:
  from flask import Flask, render_template, request, url_for
  from flask import request, jsonify
  from flask_cors import CORS
  from flask_mail import Mail, Message
  import bcrypt
except Exception as e:
  print("You're missing some modules, or you may not be using your virtualenv.")
  print(e)
  exit()
  
try:
  from secrets import SECRET_KEY
  from models import *
except Exception as e:
  print("You're missing some required files from this project.")
  print(e)
  exit()
  
# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = SECRET_KEY

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

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
#@app.before_first_request
#def create_user():
#    user_datastore.create_user(email='mercer@exandria.net', password='password')

# Routes
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/protected')
@login_required
def protected():
  return 'This is a protected route.'

def email(text, recipients, subject="AR-top"):
  try:
	msg = Message(subject, sender="ilovecrack@gmail.com", recipients = recipients)
	msg.body = text
	mail.send(msg)
  except Exception as e:
	app.logger.error("Failed to send email to " + str(recipients) + ":\n" + str(e))
	
	@app.route('/api/register', methods=['POST'])
	def register():
	  # Confirm the request is ok
	  try:
		email = request.form["email"]
		password = request.form["password"]
	  except:
		return jsonify(error="Malformed request; expecting email and password")
	  
	  if len(password) <= 8:
		return jsonify(error="Password does not satisfy minimum length of 8")
	  if not str.isalnum(password):
		return jsonify(error="We only allow alphanumeric characters")
	  
	  # Retrieve the user
	user = User.objects(email = email)
	if len(user) == 1:
	  return jsonify(error="Email already in use")
	
	# Hash and create user
  hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
  user_datastore.create_user(email=email, password=hashed)
  
  # TODO: error handle this. Can't tell the user you registered successfully if the email fails.
  email(recipients=[email], subject="ay whaddup", text="Hello from AR-top")
  
  return jsonify(success="Account has been created! Check your email to validate your account.")

if __name__ == '__main__':
  from argparse import ArgumentParser
  
  parser = ArgumentParser(description="Runs flask server")
  parser.add_argument("-email", nargs='+', type=str, help="Sends an email if you use commandline friendly text")
  parser.add_argument("-r", "--recipients", nargs='+', type=str, help="Who you want to send to ")
  args = parser.parse_args()
  
  if args.email is not None:
	if args.recipients is None:
	  print("Must specify recipients to send an email")
	  email(' '.join(args.email), args.recipients)
	  
  app.run()	  
