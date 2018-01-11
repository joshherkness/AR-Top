#!/bin/bash
set -e

echo "Going to Vue directory..."
cd vue
echo "Installing npm packages..."
npm install
echo "Creating production build of Vue..."
npm run build
echo "Copying index.html file..."
cp dist/index.html ../server/templates
echo "Copying js directory..."
cp -r dist/static/js ../server/static
echo "Copying css directory..."
cp -r dist/static/css ../server/static
echo "Going to server directory"
cd ../server

echo "Starting mongo in the background..."
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     echo "Mongod should be started in the background already...";;
    Darwin*)    mongod > mongo.log 2>&1 &;;
    CYGWIN*)    ./C/MongoDB/bin/mongod > mongo.log 2>&1 &;;
    MINGW*)     echo "Unsupported machine";;
    *)          echo "Unsupported machine"
esac
echo "If you want to view the mongod logs. Tail out mongo-log.txt.."

echo "Creating a virtual environment (for python)..."
virtualenv dev-en

echo "Activating the virtual environment..."
. dev-env/bin/activate

echo "Installing the required python packages..."
pip install -r requirements.txt

echo "Starting flask server"
python server.py

eval $npmInstall && $npmBuild && eval $copyHTML && eval $copyJS && eval $copyCSS && cd ../server && eval $server
