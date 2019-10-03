## OctoBot Preparation and Development Guide

### Install Dependencies

This required docker to run locally for verification before push to the Docker Hub. Install with this following command:

```console
ncl@orchestrator:~/$ sudo apt-get update
ncl@orchestrator:~/$ sudo apt-get install docker-ce docker-ce-cli containerd.io
ncl@orchestrator:~/$ sudo docker run hello-world
``` 
The detail steps can be found in this [link](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

### Download the Source Code
 
Download the whole source of OctoBot software from the GitHub.
 
```console
ncl@orchestrator:~/$ git clone https://github.com/nus-ncl/OctoBot
ncl@orchestrator:~/$ cd OctoBot/Octo-Bot/<bot_name>
```
 
### Build and Run the Specific Bot under Docker
 
Build locally the docker image (ex. **web-browsing-bot**).
 
```console
ncl@orchestrator:~/OctoBot/Octo-Bot/<bot_name>$ docker build . -t web-browsing-bot:latest
```

Check the docker image.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/<bot_name>$ docker images
REPOSITORY                     TAG                 IMAGE ID            CREATED             SIZE
web-browsing-bot               latest              53b3e078164f        2 days ago          1.1GB
python                         3                   02d2bb146b3b        2 weeks ago         918MB
```

Run locally the docker image.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/<bot_name>$ docker run web-browsing-bot:local <URL> 0
```

Check the running docker.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/<bot_name>$ sudo docker ps -a
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS                   PORTS               NAMES
acfcdc3f568f        web-browsing-bot:latest   "python -u ./main.py…"   2 days ago          Exited (0) 2 days ago                        priceless_bhaskara
```

### Push the docker image into Docker Hub

Tag and push the image with your Docker Hub repository's credential.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/<bot_name>$ docker tag 53b3e078164f ariscahyadi/web-browsing-bot:latest
ncl@orchestrator:~/OctoBot/Octo-Bot/<bot_name>$ docker login --username=ariscahyadi
ncl@orchestrator:~/OctoBot/Octo-Bot/<bot_name>$ docker push ariscahyadi/web-browsing-bot:latest
```

### Run the public docker image

Run locally the public docker image.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/<bot_name>$ docker run ariscahyadi/web-browsing-bot:latest <URL> 0
```