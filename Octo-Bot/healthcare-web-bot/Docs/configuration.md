# Configuration
There are 2 files that the program can accept, namely the login file and measurement file.
* The login file consists of the page information for selenium webdriver to login into the webpage
* The measurement file consists of the measurement information for selenium webdriver to automate the filling up of patient information

## Login File

There are a total of 3 login files for the 3 different roles --> `admin.csv`, `patient.csv` and `therapist.csv`

The `admin.csv`, `therapist.csv` and `patient.csv` files in the forked repo are not updated. Please do update it with the latest credentials for the bot to work.

There are 2 properties to be included in the login file.
* Username - username of the user for selenium webdriver to automate login process
* Password - password of the user for the selenium webdriver to automate login process

Here is an example of a sample login file. Any other fields that are inside the file will be ignored.The format of the login files are the same for `admin.csv`, `patient.csv` and `therapist.csv`.
```csv
<username>, <password>
<username>, <password>
<username>, <password>
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
      "measurement": "30",
      "title": "NIL",
      "description": "NIL"
    },
    "weight": {
      "measurement": "50",
      "title": "NIL",
      "description": "NIL"
    },
    "temperature": {
      "measurement": "40",
      "title": "NIL",
      "description": "NIL"
    },
    "blood pressure": {
      "systolic": "20",
      "diastolic": "20",
      "title": "NIL",
      "description": "NIL"
    }
}
```

