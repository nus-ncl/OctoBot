# Configuration
There are 2 files that the program can accept, namely the login file and measurement file.
* The login file consists of the page information for selenium webdriver to login into the webpage
* The measurement file consists of the measurement information for selenium webdriver to automate the filling up of patient information
* There can be multiple login files with the name `login<number>.json`, but there can only be 1 measurement file

## Login File

There are 3 properties to be included in the login file.
* Username - username of the user for selenium webdriver to automate login process
* Password - password of the user for the selenium webdriver to automate login process
* url - url of the development server

Here is an example of a sample login file. Any other fields that are inside the file will be ignored.
```json
{
  "url": "http://10.10.0.112",
  "user1": ["<username1>", "<password1>"],
  "user2": ["<username2>", "<password2>"],
  "user3": ["<username3>", "<password3>"],
  "user4": ["<username4>", "<password4>"],
  "user5": ["<username5>", "<password5>"]
}
```

## Measurement File

There are 4 properties to be included in the measurement file.
* Height : Each of the height attribute will be associated with a ```measurement```, ```title``` and ```description```
* Weight : Each of the weight attribute will be associated with a ```measurement```, ```title``` and ```description```
* Temperature : Each of the temperature attribute will be associated with a ```measurement```, ```title``` and ```description```
* Blood Pressure : Each of the blood pressure attribute will be associated with a ```systolic```, ```diastolic```, ```title``` and ```description```

Here is an example of the sample measurement file. Any other fields that are inside this file will be ignored.
```json
{
    "height": {
      "measurement": "<height value>",
      "title": "<title of record>",
      "description": "<description of record>"
    },
    "weight": {
      "measurement": "<weight value>",
      "title": "<title of record>",
      "description": "<description of record>"
    },
    "temperature": {
      "measurement": "<temperature value>",
      "title": "<title of record>",
      "description": "<description of record>"
    },
    "blood pressure": {
      "systolic": "<systolic blood pressure value>",
      "diastolic": "<diastolic blood pressure value>",
      "title": "<title of record>",
      "description": "<description of record>"
    }
}
```

