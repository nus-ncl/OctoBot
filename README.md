# Web Browsing Bot

## Prerequisites
Ensure that the following is installed
* Docker ([How to install](https://docs.docker.com/install/ "https://docs.docker.com/install/"))

## Installing
Build the docker image
```console
./build.sh
```

## Usage
Run the docker image
```console
sudo docker run -it web-browsing-bot <url>
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
        "url": "http://localhost:8000/setup",
        "actions" : [
            {"id": "ctf_name", "action": "click"},
            {"name": "ctf_description", "value": "Setting up CTF automatically"},
            {"css": "body > #id", "key": "ENTER BACK_SPACE"}
        ]
    },
    {
        "url": "http://localhost:8000/admin/challenges/new",
        "actions": [
            {"id": "ctf_name", "action": "click"},
            {"name": "ctf_description", "value": "Setting up CTF automatically"},
            {"css": "body > #id", "key": "ENTER BACK_SPACE"}
        ]
    }
]
```
There are 3 types of selectors in this file: id, name and css
#### id
This will select the element based on the id attribute.

#### name
The element will be selected based on the name attribute

#### css
The element will be selected based on the css selector provided

There are 3 types of actions: value, action, key
#### Value
The element selected will be filled with the provided value using [sendKeys()](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html#sendKeys-java.lang.CharSequence...- "sendKeys() documentation") method provided by selenium

The value of this attribute can be a string or an array of strings.

#### Action
The provided action will be done on the selected element.
Note: Currently only "click" is supported. The element will be clicked using the [click()](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html#click-- "click() documentation" ) method provided by selenium

#### Key
Space-separated keys that will be passed into [valueOf()](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/Keys.html#valueOf-java.lang.String-) method.

### Login file
Below is an example of the login file
```json
{
    "loginAction": 
    {
        "url": "http://localhost:8000/login",
        "actions": [
            {"name": "name", "value": ["admin"]},
            {"name": "password", "value": ["admin"]},
            {"css": "button[type='submit'", "action": "click"}
        ]
    },
    "logoutAction":{
        "url": "http://localhost:8000/logout"
    }
}
```
The actions property is exactly the same as the one in the action file. 
