# Usage
Here is the help page for the healthcare-web-bot program:
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -h
usage: main.py [-h] [-t time] [-r role] [-b bot] [-u username] [-p password]
               [-m mode of execution]

Arguments for program

optional arguments:
  -h, --help            show this help message and exit
  -t time               Time to sleep between crawling of website links
  -r role               Role that the bot should login as
  -b bot                Number of credentials for the choosen role
  -u username           Username to be used for login
  -p password           Password to be used for login
  -m mode of execution  Mode for bot to be executed(daemon | non-daemon)
```

## Examples

## Crawl with waiting time in between website links
This allows the bot to crawl website links with a specified sleep time between crawling. The default value is set to 0, if this field is not specified.
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -t 20
```

## Crawl the website with a specified role
This allows the bot to crawl the website using an intended role. The roles available are "admin", "patient", and "therapist". The bot will take on the default role of an admin if this is not specified.
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -r admin
```

## Crawl the website with multiple bots in parallel
Specify the number of parallel bots that are to be run at the same time. The default value is set to 1 if this field is not specified.
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -b 5
```

## Crawl the bot with specified username and password
Specify the username and password to login and crawl the website. The bot will login from the csv list of usernames and passwords if this is not specified.
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -u <username> -p <password>
```

## Execute the bot in a daemon mode
The bot will start to execute in daemon mode and start to run in the background in another thread. This argument is optional and should only be specified if the user wants to run the bot in daemon mode.
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -m daemon
```
