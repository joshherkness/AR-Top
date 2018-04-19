cd vue
sudo docker build -t oakland/vue .
cd ../server
sudo docker build -t oakland/flask . -f Dockerfile-flask
sudo docker build -t oakland/sockets . -f Dockerfile-sockets
