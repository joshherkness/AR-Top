# Server

Included packages include:

- `flask-security`
- `flask-mongoengine`

## Setting up a development environment

Make sure to install `MongoDB` and `virtualenv`

```
# Create a virtual environment (for python)
virtualenv dev-env

# Activate the virtual environment
. dev-env/bin/activate

# Install the required pyhton packages
pip install -r requirements.txt
```

## Running the server

The server should open at `http://localhost:5000/`

```
# Activate the virtual environment
`. dev/bin/activate`

# Start the mongodb database
mongod #on mac

# Start the flask server
python server.py
```

## Adding a python module `important`

When you add a python module, make sure that the `requirements.txt` is updated.

```
# Update requirements.txt
pip freeze > requirements.txt
```
