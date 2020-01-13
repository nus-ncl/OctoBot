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
usage: prog [-h] [-b browser_name] [-c] [-d depth] [-o] [-t TIME] [-l login_file] [-a action_file] url

Bot that browses the web

positional arguments:
  url                    URL to crawl and do actions

named arguments:
  -h, --help             show this help message and exit
  -b browser_name, --browser browser_name
                         Browser to utilise
  -c, --crawl            Boolean on whether to crawl first or not
  -d depth, --depth depth
                         Depth to crawl website from entrypoint
  -o, --other-domain     Allow to crawl to different domain
  -t TIME, --time TIME   Max time to browse (seconds)
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
#### URL Selector
There are two properties that can be used to select the URL. The values of these properties can also be written using [java regex](https://docs.oracle.com/javase/7/docs/api/java/util/regex/Pattern.html)
* **url** - Full URL to match
* **path** - Matches only the path portion of the file

The following are all acceptable URL selectors.
```json
"path": "/setup"
"url": "http://localhost:8000/setup"
"path": "/setup/.*"
"url": "http://localhost:8000/setup/.*"
```

#### Actions
In the actions property, it is an array of actions. Every action has two groups of properties: selector and action.
```json
"actions":[
	{"<selector>": "value", "<action>": "value"},
	{"<selector>": "value", "<action>": "value"}
]
```

##### Selector
There are 3 types of selectors in this file: id, name and css
* **id** - Select element based on the id attribute
* **name** - Select element based on the name attribute
* **css** - Select element based on [css selector]("https://www.w3schools.com/cssref/css_selectors.asp" "CSS Selector Reference")

##### Action
There are 3 types of actions: value, action, key
* **value** - The provided value will fill the selected element using the [sendKeys()](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html#sendKeys-java.lang.CharSequence...- "sendKeys() documentation") method. The value of this attribute can be a **string** or an **array of strings**.
* **action** - The provided action will be done on the selected element. Currently only "[click](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html#click-- "click() documentation")" is supported. 
* **key** - Space-separated name of the enum constant that will be passed into [valueOf()](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/Keys.html#valueOf-java.lang.String-) method to be executed on the selected element.

All of these are acceptable values for the actions property.
```json
"actions":[
	{"name": "username", "value": ["admin", "user"]},
	{"id": "password", "value": "password"},
	{"css": "#submitBtn", "action": "click"},
	{"css": "body > .modal > input[name='field']", "key": "BACK_SPACE ENTER"}
]
```
#### Putting it together
Here is what a sample action file look like. Any other properties other than those specified above will be ignored.
```json
[
    {
        "comments": "Initial setup of CTF",
        "path": "/setup",
        "actions" : [
            {"id": "ctf_name", "value": "MyCTF"},
            {"id": "ctf_name", "key": "ENTER"},
            {"css": "#general > div.float-right > button", "action": "click"}
        ]
    },
    {
        "path": "/admin/challenges/new",
        "actions": [
            {"id": "create-chals-select", "value": "dynamic"},
            {"name": "name", "value": ["Challenge #1", "Challenge #2"]}
       	]
    }
]
```

### Login file
The login file is similar to the action file, with a few additions.
1. Every object has two properties: loginAction and logoutAction
2. The object within the loginAction and logoutAction is exactly the same as that of the action file.

Below is an example of the login file. As we can see, it is possible to have multiple login credentials.
```json
[{
    "loginAction": 
    {
        "path": "/login",
        "actions": [
            {"name": "name", "value": ["admin", "john"]},
            {"name": "password", "value": ["admin", "john"]},
            {"css": "button[type='submit']", "action": "click"}
        ]
    },
    "logoutAction":{
        "path": "/logout"
    }
}]
```

Multiple login objects are able to be declared too, if a webpage has multiple login pages.
```json
[{
    "loginAction": 
    {
        "path": "/login",
        "actions": [
            {"name": "name", "value": ["admin", "john"]},
            {"name": "password", "value": ["admin", "john"]},
            {"css": "button[type='submit']", "action": "click"}
        ]
    },
    "logoutAction":{
        "path": "/logout"
    }
},
{
    "loginAction": 
    {
        "path": "/login2",
        "actions": [
            {"name": "name", "value": "admin2"},
            {"name": "password", "value": "admin2"},
            {"css": "button[type='submit']", "action": "click"}
        ]
    },
    "logoutAction":{
        "path": "/logout2"
    }
}]
```
## Frequently Asked Questions (FAQ)
Question: How do I determine the CSS selector of elements

Answer: Most modern browsers support this feature. Open "inspect element" and hover over the intended element, right click and there should be a option to copy the css selector. Below shows some examples on some browsers.

**Firefox**
![Copying css selector in firefox](resources/gif/CSS_Selector_Firefox.gif)

**Chrome**
![Copying css selector in chrome](resources/gif/CSS_Selector_Chrome.gif)

## Known issues
* If firefox keeps crashing in docker, adding `--shm-size 2g` or `-v /dev/shm:/dev/shm` to the `docker run` command will stop it from crashing ([More information here](https://github.com/SeleniumHQ/docker-selenium/pull/485))