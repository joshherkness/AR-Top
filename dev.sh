#!/bin/bash
set -e

echo "Going to server directory..."
cd server

echo "Creating a virtual environment (for python)..."
virtualenv dev-en

echo "Activating the virtual environment..."
. dev-env/bin/activate

echo "Installing the required python packages..."
pip install -r requirements.txt

echo "Starting mongo in the background..."
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     echo "Mongod should be started in the background already...";;
    Darwin*)    mongod > mongo.log 2>&1 &;;
    CYGWIN*)    ./C/MongoDB/bin/mongod > mongo.log 2>&1 &;;
    MINGW*)     echo "Unsupported machine";;
    *)          echo "Unsupported machine"
esac

echo "If you want to view the mongod logs. Tail out mongo-log.log..."

echo "Starting Flask server.."
python server.py > flask.log 2>&1 & #Pipe flask stdout and stderr to log file.
echo "If you want to view the Flask logs. Tail out flask-log.log..."

echo "Going to the Vue directory..."
cd ../vue

echo "Installing nmp packages..."
npm install

echo "Starting npm dev environment..."
npm run dev

#eval $virtualEnv && eval $activateVirtualEnv && eval $pip && eval $mongo && eval $server && cd ../vue && eval $npmInstall && eval $npmDev

trap 'kill $(jobs -p)' EXIT
