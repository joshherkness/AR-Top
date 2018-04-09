# AR-Top

### Define your world

AR-Top is a suite of Augmented Reality (AR) tabletop applications consisting of two parts. 
First, a web experience is used to edit maps within a 3D environment as well as host session for others to join. 
Second, a mobile application is used to join sessions and view those maps in an augmented reality environment.

1. [Setting up](#setup)
	1. [Server deployment](#server-deployment)
	2. [Getting the mobile app](#getting-the-mobile-app)
2. [Usage](#running)
3. [Group members](#group-members)

Setting up
==========

Server deployment
---------

1. Download [docker](https://docs.docker.com/install/) for your server.
2. Run our ```build-docker``` script from the application root. 
	1. Before you run it, you may want to [add docker to sudo](https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo?answertab=votes#tab-top), but this can pose a security risk on your machine. This step is optional.
3. ```docker-compose up``` will start the server. Run with the ```-d``` flag to daemon it.

Getting the Mobile App
----------------------

1. Android users download the APK. iPhone users must build from source.
2. Correct this cuz Im sure its wrong

Running
=======

1. Connect to the server's IP address.
2. Create a map (picture maybe)
3. Create a session (picture maybe)
	1. The session, once created, will generate a code.
4. Use the mobile app to join the session, given the code.

Group members
=============

[Joshua Herkness](https://github.com/joshherkness)

[KaJuan Johnson](https://github.com/kdjohnson)

[Johnathan Robertson](https://github.com/jjrobertson14)

[Anthony Hewins](https://github.com/AnthonyHewins)

[Neil Ferman](https://github.com/goeteeks)

[Trevor Luebbert](https://github.com/TrevorLuebbert)

## Future plans

While the application is tailored towards use in tabletop games such as Dungeons & Dragons (D&D), if the design is also altered, it has implications in fields such as prototyping and architecture.