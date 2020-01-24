# Web Browsing Bot

## Prerequisites
Ensure that the following is installed
1. Docker ([How to install](https://docs.docker.com/install/ "https://docs.docker.com/install/"))
2. Git

## Installing
Installing git
```console
whyare@BrowsingBot:~$ sudo apt update && sudo apt install git
```

Build the docker image
```console
whyare@BrowsingBot:~$ git clone https://github.com/WhyAre/webbrowsingbot.git
whyare@BrowsingBot:~$ cd webbrowsingbot/
whyare@BrowsingBot:~/webbrowsingbot$ ./build.sh
```

## Usage
View all the options
```console
whyare@BrowsingBot:~$ docker run -it --rm browsing-bot -h
usage: prog [-h] [-b BROWSER_NAME] [-c] [-d DEPTH] [-H] [-o] [-t DURATION] [-T [USERNAME]] [-u USER_AGENT] [-l LOGIN_JSON]
            [-a ACTION_JSON] url

Bot that browses the web

positional arguments:
  url                    URL to crawl and do actions

named arguments:
  -h, --help             show this help message and exit
  -b BROWSER_NAME, --browser BROWSER_NAME
                         Browser to utilise (Default chrome)
  -c, --crawl            Boolean on whether to crawl first or not
  -d DEPTH, --depth DEPTH
                         Depth to crawl website from entrypoint
  -H, --headless         Boolean to launch browser in headless mode
  -o, --other-domain     Allow to crawl to different domain
  -t DURATION, --time DURATION
                         Max time to browse (seconds)
  -T [USERNAME], --test [USERNAME]
                         Test user actions
  -u USER_AGENT, --user-agent USER_AGENT
                         User agent to use
  -l LOGIN_JSON, --login LOGIN_JSON
                         JSON configuration for login
  -a ACTION_JSON, --action ACTION_JSON
                         JSON configuration for actions
```

Run the docker image without options
```console
whyare@BrowsingBot:~$ sudo docker run -it --rm browsing-bot <url>
```

## Sample
Clone CTFd repository and bring it up
```console
whyare@BrowsingBot:~$ git clone https://github.com/CTFd/CTFd.git
whyare@BrowsingBot:~$ cd CTFd/
whyare@BrowsingBot:~/CTFd$ docker-compose up
```

Run the web-browsing-bot
```console
whyare@BrowsingBot:~/webbrowsingbot/sample$ sudo docker run -it --rm \
browsing-bot \
--login "$(ctfd_login.json)" \
--action "$(ctfd_action.json" \
<ip_address>:8000
```

## Documentation
Detailed documentation and more samples can be found on the [Docs](https://github.com/WhyAre/browsing-bot/tree/master/Docs).
