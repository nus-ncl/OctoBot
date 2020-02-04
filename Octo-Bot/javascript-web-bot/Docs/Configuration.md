# Configuration
There are 2 files that the program can accept, namely the login file and action file.
* The action file consists of the page actions for selenium webdriver to do when it reaches that page
* The login file consists of the login information and actions to carry out on the login/logout page using selenium

## Action file
### URL Selector
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

### Actions
In the actions property, it is an array of actions. Every action has two groups of properties: selector and action.
```json
"actions":[
	{"<selector>": "value", "<action>": "value"},
	{"<selector>": "value", "<action>": "value"}
]
```

#### Selector
There are 3 types of selectors in this file: id, name and css
* **id** - Select element based on the id attribute
* **name** - Select element based on the name attribute
* **css** - Select element based on [css selector]("https://www.w3schools.com/cssref/css_selectors.asp" "CSS Selector Reference")

#### Action
There are 3 types of actions: value, action, key
* **value** - The provided value will fill the selected element using the [sendKeys()](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html#sendKeys-java.lang.CharSequence...- "sendKeys() documentation") method. The value of this attribute can be a **string** or an **array of strings**.
* **action** - The provided action will be done on the selected element. The possible values are [click](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html#click--), [clear](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html#clear--) or [submit](https://selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html#submit--).  
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
### Putting it together
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

## Login file
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