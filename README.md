#  UNOFFICIAL REST API FOR LOST ARK

![alt text](https://images.ctfassets.net/umhrp0op95v1/S3yKwaVAOi8Bgqg4n4scf/adae769671b271b88f97d31721432986/LA_LOGO.png)

An Unofficial REST API for [LOST ARK](https://www.playlostark.com/en-us/news)

You can run the REST API on a service like [Heroku](http://lostarkapi.herokuapp.com/) or on your local machine.

[![Deploy To Heroku](https://camo.githubusercontent.com/c0824806f5221ebb7d25e559568582dd39dd1170/68747470733a2f2f7777772e6865726f6b7563646e2e636f6d2f6465706c6f792f627574746f6e2e706e67)](https://heroku.com/deploy)

# Features
This REST API provides you with some useful tools such as:
- Server Status
- Latest News
- Forum topics and specific Forums

# Requirements
You are required to have Python3 and pip installed.

If you wish to run this process in docker, you are required to download [Docker](https://www.docker.com/).
- Docker for Windows / Mac: [Download Page](https://www.docker.com/get-started)
- Linux
    - Ubuntu: [`https://docs.docker.com/engine/install/ubuntu/`](https://docs.docker.com/engine/install/ubuntu/)
    - Debian: [`https://docs.docker.com/engine/install/debian/`](https://docs.docker.com/engine/install/debian/)

Once you have everything installed, you need to download the below recommended modules.

# Recommended modules

The following modules represent the minimum version required to run this REST API.
- requests (2.27.1)
- fastapi (0.73.0)
- uvicorn[standard] (0.17.4)
- beautifulsoup4 (4.10.0)
- lxml (4.7.1)
- ujson (5.1.0)

When installing the above modules in pip, you can run a command similar to this:
`pip install [Module]==[Version]`

Example: `pip install requests==2.27.1`

Or you can download the latest version by simply `pip install requests`

# Execution

When everything above is installed correctly, you can simply run the `main.py` application.

Please follow the [**Docker Guide**](https://docs.docker.com/get-docker/) on how to set up your Docker environment.

# Maintainers
This Repo has been developed and maintained by [**Andre Saddler**](https://github.com/axsddlr).
