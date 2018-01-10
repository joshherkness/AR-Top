#!/bin/bash

npm="npm run build"
copyJS="cp -r dist/static/js ../server/static"
copyCSS="cp -r dist/static/css ../server/static"
copyHTML="cp dist/index.html ../server/templates"
server="python3 server.py"
cd vue

eval $npm && eval $copyHTML && eval $copyJS && eval $copyCSS && cd ../server && eval $server

