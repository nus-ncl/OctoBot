## Developing the Bot:

Create a local build of the docker image:

```console
joelczk@OctoBot:~$ cd OctoBot/Octo-Bot/<bot-name>
joelczk@OctoBot/Octo-Bot/<bot-name>:~/OctoBot$ docker build . -t web-crawler:latest
```

Check the local image:

```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker images
REPOSITORY                     TAG                 IMAGE ID            CREATED             SIZE
web-crawler                    latest              f112835c8a07        1 days ago          1.1GB
python                         3.8-alpine3.10      02d2bb146b3b        2 weeks ago         918MB
```

Run the docker image:

```console
joelczk@OctoBot/Octo-Bot/<bot-name>:~/OctoBot$ docker run web-crawler
```

Check the running container:

```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ sudo docker ps -a
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS                   PORTS               NAMES
acfcdc3f568f        web-crawler:latest   "python -u ./main.py…"   2 days ago          Exited (0) 2 days ago                        priceless_bhaskara
```
