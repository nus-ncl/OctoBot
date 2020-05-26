## OctoBot Quick Start Guide

### Install Dependencies

We should verify that the container works locally before we push it to Docker Hub. On Ubuntu, install `docker` with this following command:

```console
ncl@orchestrator:~/$ sudo apt-get update
ncl@orchestrator:~/$ sudo apt-get install docker-ce docker-ce-cli containerd.io
ncl@orchestrator:~/$ sudo docker run hello-world
``` 
The detail steps can be found in this [link](https://docs.docker.com/install/linux/docker-ce/ubuntu/).
For other Linux distros, visit [link](https://docs.docker.com/engine/install/). (It is not recommended to use a non-posix OS like Windows for this)

### Download the Source Code
 
Download the whole source of OctoBot software from the GitHub and navigate to the specific directory
 
```console
ncl@orchestrator:~/$ git clone https://github.com/nus-ncl/OctoBot
ncl@orchestrator:~/$ cd OctoBot/Octo-Bot/packet-generator-bot
```
 
### Build and Run the Specific Bot under Docker
 
Build the docker image locally.
 
```console
ncl@orchestrator:~/OctoBot/Octo-Bot/packet-generator-bot$ ./build.sh
```

Check the docker image.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/packet-generator-bot$ docker images
REPOSITORY                     TAG                 IMAGE ID            CREATED             SIZE
packet-generator-bot           latest              529fceb6545d        8 minutes ago       118MB
debian                         buster-slim         108d75da320f        8 days ago          69.2MB

```

Run the docker image locally.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/packet-generator-bot$ docker run packet-generator-bot:latest -r captures/<pcap file>
```

Check the running docker.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/packet-generator-bot$ sudo docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS                      PORTS               NAMES
888677a369da        packet-generator-bot:latest   "python3 main.py -r …"   38 seconds ago      Exited (0) 40 seconds ago                       tony_stark
```

### Push the docker image into Docker Hub

Tag and push the image with your Docker Hub repository's credential. Replace `korona` with your own username on Docker Hub.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/packet-generator-bot$ docker tag 529fceb6545d korona/packet-generator-bot:latest
ncl@orchestrator:~/OctoBot/Octo-Bot/packet-generator-bot$ docker login --username=korona
ncl@orchestrator:~/OctoBot/Octo-Bot/packet-generator-bot$ docker push korona/packet-generator-bot:latest
```

### Run the public docker image

Run locally the public docker image.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/packet-generator-bot$ docker run korona/packet-generator-bot:latest -r captures/http.cap -a 192.168.0.1 -A 192.168.1.254
```