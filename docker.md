# Docker

## Install Docker CE

* Docker can be installed [here](https://docs.docker.com/install/). Select your appropriate operating system.

* Ensure you have Docker Compose as well.

## Getting to know Docker

* Read some of the basic concepts of docker [here](https://docs.docker.com/get-started/#docker-concepts)

## Building the vue image

* Go to the `vue` directory. You will see that we have a [Dockerfile](vue/Dockerfile) that defines our container.

* To build our image run the following command:

```
docker build -t oakland/vue .
```

Run the command `docker images`. You should see something similar to this.

```

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
oakland/vue         latest              8fa22c876cae        3 minutes ago       376MB
node                alpine              a88ff852e3d4        3 hours ago         68MB
```

## Building the Flask image

* Go the the `server` directory where you will find two Dockerfiles, We will use the [Dockerfile-flask](server/Dockerfile-flask) file.

* To build our image run the following command:

```
docker build -t oakland/flask . -f Dockerfile-flask
```

Run the `docker images` command. You should see something similar:

```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
oakland/flask       latest              4c4ba5679d46        5 minutes ago       782MB
oakland/vue         latest              8fa22c876cae        21 minutes ago      376MB
node                alpine              a88ff852e3d4        3 hours ago         68MB
python              jessie              336d482502ab        6 days ago          692MB
```

## Building the Flask SocketIO image

* Go the the `server` directory where you will find two Dockerfiles, We will use the [Dockerfile-sockets](server/Dockerfile-sockets) file.

* To build our image run the following command:

```
docker build -t oakland/sockets . -f Dockerfile-sockets
```

Run `docker images`. You should see something similar.

```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
oakland/sockets     latest              71759bb5f9b9        2 seconds ago       782MB
oakland/flask       latest              4c4ba5679d46        9 minutes ago       782MB
oakland/vue         latest              8fa22c876cae        25 minutes ago      376MB
node                alpine              a88ff852e3d4        3 hours ago         68MB
python              jessie              336d482502ab        6 days ago          692MB
```

## Docker Compose

* We currently have a multi-container Docker application. So to easily start all of our services we will use [Docker Compose](https://docs.docker.com/compose/overview/)

* To start Docker Compose run the following:

```
docker-compose up
```
Go to [localhost](http://localhost) in your browser.

## Wrapping up

* Should you ever make a change to one of the images you will need to rebuild it for Docker Compose to recognize those changes.

* To remove dangling and unused images use `docker system prune -a`

* To see running containers use `docker ps`

* If while closing Docker Compose and it doesn't stop the currently running containers use `docker-compose kill` to stop them.

* If you want to enter into a running container you first need to have it's container id. So run `docker ps` to view all running containers and view their ids.

    *  For the python containers:

        * `docker exec -it CONTAINER_ID /bin/bash`

    * For the mongo container:

        * `docker exec -it CONTAINER_ID mongo`

    * For the vue container:

        * `docker exec -it CONTAINER_ID /bin/ash`