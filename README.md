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
sudo docker run -it browsing-bot <url>
```

## Sample
Enter the sample folder and run docker-compose to run the CTFd
```console
cd sample/CTFd
docker-compose up
```

Run the web-browsing-bot. (Please enter the json files and change "localhost" to the relevant IP address
```console
sudo docker run -it -v $(pwd):/utils browsing-bot --login /utils/ctfd_login.json --action /utils/ctfd_action.json <ip_address>:8000
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
        "url": "http://localhost:8000/login",
        "actions": [
            {"name": "name", "value": ["admin"]},
            {"name": "password", "value": ["admin"]},
            {"css": "button[type='submit']", "action": "click"}
        ]
    },
    "logoutAction":{
        "url": "http://localhost:8000/logout"
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
