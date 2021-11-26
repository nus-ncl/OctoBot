# Web-based Banking Application Bot
The bot is specially built for Terracotta web-based banking application.

## Terracotta Banking Application Setup
Detailed information about Terracotta Bank can be found here https://github.com/terracotta-bank/terracotta-bank.git

### Prerequisites
Ensure that the following is installed:

1. Git
2. Java 8

### Download and Run
```
git clone https://github.com/terracotta-bank/terracotta-bank.git
cd terracotta-bank/terracotta-bank-servlet
./gradlew bootRun
```

## Run Terracotta Web Application Bot with Docker
It is recommended to run the bot using Docker container.

### Prerequisites
Ensure that the following is installed:

1. Git
2. Docker ([How to install](https://docs.docker.com/install/))

### Installation
Build

```
git clone https://github.com/nus-ncl/OctoBot.git
cd OctoBot/Octo-Bot/banking-web-application-bot
docker build -t terracotta-bot .
```

Run

```
docker run --network="host" terracotta-bot:latest
```

View All Options
```
docker run --network="host" terracotta-bot:latest -h
usage: main.py [-h] [-url url of application] [-wf workflow to use]
               [-u username] [-orgPass password] [-p new password]
               [-n name of user] [-e email of user] [-u2 username of B]
               [-p2 password of B] [-u3 username of Parent]
               [-p3 password of Parent] [-d display] [-a amount] [-l amount]

Arguments for program

optional arguments:
  -h, --help            show this help message and exit
  -url url of application
                        Target Website URL
  -wf workflow to use   Workflow for this bot
  -u username           Username to be used
  -orgPass password     Password to be used
  -p new password       New password to be changed to
  -n name of user       Name to be used
  -e email of user      Email to be used
  -u2 username of B     Username to be used
  -p2 password of B     New password to be changed to
  -u3 username of Parent
                        Username to be used
  -p3 password of Parent
                        New password to be changed to
  -d display            Time to sleep between crawling of website links
  -a amount             Amount to deposit or transfer
  -l loop             Loop workflow



```

### Sample Usage

Run create and change password workflow for user A
```
docker run --network="host" terracotta-bot:latest -wf password
```

Create account for user B
```
docker run --network="host" terracotta-bot:latest -wf create -u test-2 -p Password@2 -e test-2@test.com -n test-2
```

Create account for parent
```
docker run --network="host" terracotta-bot:latest -wf create -u test-3 -p Password@3 -e test-3@test.com -n parent
```

Run deposit workflow using A into B
```
docker run --network="host" terracotta-bot:latest -wf deposit
```

Run transfer workflow from A to B
```
docker run --network="host" terracotta-bot:latest -wf transfer
```

Run parent-subsidiary workflow (Parent deposit into A and A transfer to B)
```
docker run --network="host" terracotta-bot:latest -wf parentSub
```

NOTE: For the latter three workflows, if no username and password arguments are specified via command line, these are the credentials set as default so ensure these accounts are created:
- User A (Username: test-1 Password: Password@1)
- User B (Username: test-2 Password: Password@2)
- Parent (Username: test-3 Password: Password@3)



## Run Terracotta Web Application Bot Natively
If there is a problem to build and run the Bot through Docker, the Bot also can be run natively (without Docker)

### Install Python and its dependencies
Installing git

```
sudo apt update && sudo apt install git
```

Installing pip

```
sudo apt install python3-pip
```

Installing Python dependencies

```
sudo apt-get install python3-tk python3-dev
```

### Install Selenium Web Driver
Install Web driver

```
wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz
sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.23.0-linux64.tar.gz -O /usr/bin/geckodriver'
sudo chmod +x /usr/bin/geckodriver
rm geckodriver-v0.23.0-linux64.tar.gz
```

Installing Python packages (Selenium, Numpy, ...)

```
pip install selenium==3.141.0 --upgrade cryptography
pip install numpy
pip install pyautogui
pip install bezier
```

### Running the Bot
View all the options

```
git clone https://github.com/nus-ncl/OctoBot.git
cd OctoBot/Octo-Bot/banking-web-application-bot
python3 main.py -d 1
```

