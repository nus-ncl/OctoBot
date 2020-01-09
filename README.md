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
whyare@BrowsingBot:~$ sudo docker run -it browsing-bot -h
usage: prog [-h] [-b browser_name] [-c] [-d depth] [-l login_file] [-a action_file] url

Bot that browses the web

positional arguments:
  url                    URL to crawl and do actions

named arguments:
  -h, --help             show this help message and exit
  -b browser_name, --browser browser_name
                         Browser to utilise
  -c, --crawl            Boolean on whether to crawl first or not
  -d depth, --depth depth
                         Max depth to crawl
  -l login_file, --login-file login_file
                         File that contains login credentials
  -a action_file, --action-file action_file
                         File that contains actions to do on selected page(s)
```

Run the docker image without options
```console
whyare@BrowsingBot:~$ sudo docker run -it browsing-bot <url>
```

## Sample
Enter the sample folder and run docker-compose to run the CTFd
```console
whyare@BrowsingBot:~/webbrowsingbot$ cd sample/CTFd
whyare@BrowsingBot:~/webbrowsingbot/sample/CTFd$ docker-compose up
```

Run the web-browsing-bot
```console
whyare@BrowsingBot:~/webbrowsingbot/sample$ sudo docker run -it \
-v $(pwd):/utils \
browsing-bot \
--login /utils/ctfd_login.json \
--action /utils/ctfd_action.json \
<ip_address>:8000
```


## Configuration
There are 2 files that the program can accept, namely the login file and action file.
* The action file consists of the page actions for selenium webdriver to do when it reaches that page
* The login file consists of the login information and actions to carry out on the login/logout page using selenium

### Action file
Below is a sample of an action file
```json
[
    {
        "path": "/setup",
        "actions" : [
            {"id": "ctf_name", "action": "click"},
            {"name": "ctf_description", "value": "Setting up CTF automatically"},
            {"css": "body > #id", "key": "ENTER BACK_SPACE"}
        ]
    },
    {
        "path": "/admin/challenges/new",
        "actions": [
            {"id": "ctf_name", "action": "click"},
            {"name": "ctf_description", "value": ["Setting up CTF automatically", "Text #2"]},
            {"css": "body > #id", "key": "ENTER BACK_SPACE"}
        ]
    }
]
```
Every action has two components: a selector and an action
```json
{"selector": "value", "action": "value"}
```
##
#### Selector
There are 3 types of selectors in this file: id, name and css
* **id** - Select element based on the id attribute
* **name** - Select element based on the name attribute
* **css** - Select element based on [css selector]("https://www.w3schools.com/cssref/css_selectors.asp" "CSS Selector Reference")

##
#### Action
There are 3 types of actions: value, action, key

* **value** - The provided value will fill the selected element using the [sendKeys()](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html#sendKeys-java.lang.CharSequence...- "sendKeys() documentation") method. The value of this attribute can be a string or an array of strings.
* **action** - The provided action will be done on the selected element. Currently only "[click](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html#click-- "click() documentation")" is supported. 
* **key** - Space-separated name of the enum constant that will be passed into [valueOf()](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/Keys.html#valueOf-java.lang.String-) method to be executed on the selected element.
##
### Login file
Below is an example of the login file
```json
{
    "loginAction": 
    {
        "path": "/login",
        "actions": [
            {"name": "name", "value": ["admin"]},
            {"name": "password", "value": ["admin"]},
            {"css": "button[type='submit']", "action": "click"}
        ]
    },
    "logoutAction":{
        "path": "/logout"
    }
}
```
The actions property is exactly the same as the one described in the action file. 

## Frequently Asked Questions (FAQ)
Question: How do I determine the CSS selector of elements

Answer: Most modern browsers support this feature. Open "inspect element" and hover over the intended element, right click and there should be a option to copy the css selector. Below shows some examples on some browsers.

**Firefox**
![Copying css selector in firefox](resources/gif/CSS_Selector_Firefox.gif)

**Chrome**
![Copying css selector in chrome](resources/gif/CSS_Selector_Chrome.gif)
