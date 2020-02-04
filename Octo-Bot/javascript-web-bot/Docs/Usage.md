# Usage
Here is the help page for the program
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

#### URL
URL to crawl. This program is not very strict in URL convention. https://www.google.com, http://www.google.com or www.google.com are acceptable values.

#### -b, --browser=BROWSER
Choose which browser to use. Values: ```firefox``` or ```chrome```

#### -c, --crawl
Choose whether to crawl or not

#### -d, --depth=DEPTH
An integer which states how deep for the crawler to crawl. Only works when the ```--crawl``` option is specified.

#### -o, --other-domain
Allows the crawler to access websites that belongs to a different domain

#### -t, --time=DURATION
Integer, in seconds, on the duration the bot will browse for.

#### -T, --test=USERNAME
Tests the ```--login``` and ```--action``` actions (if applicable) without browsing. USERNAME refers to the user that the bot will log in into to test the actions.

#### -u, --user-agent=USERAGENT
Specifies the useragent string the bot will use to browse the web. Read more about use agent [here](https://en.wikipedia.org/wiki/User_agent "User-agent - Wikipedia")

#### -l, --login=LOGIN_JSON
JSON string of the login and logout actions. Read more about the configurations [here](Configuration)

#### -a, --action=ACTION_JSON
JSON string of the actions to be conducted by the bot. Read more about the configurations [here](Configuration)

# Examples

## Normal browsing
This is the normal operation when no flags are passed to it. The bot will find for links to visit and visit random pages until either time is up or user interrupts it.
```console
whyare@BrowsingBot:~$ sudo docker run -it --rm browsing-bot <website_name>
```

## Browse with crawl
The ```--crawl``` option can be specified to crawl the website first before browsing.
```console
whyare@BrowsingBot:~$ sudo docker run -it --rm browsing-bot --crawl <website_name>
```

## Browse with actions
The program accepts json strings as input.
```console
whyare@BrowsingBot:~/webbrowsingbot/sample$ sudo docker run -it --rm browsing-bot \
--action "<json_string_here>" \
<website_name>
```

However, as json string can get long and complicated, it is recommended to put the json string in the file and then using the ```cat``` command to direct content as input of the program.
```console
whyare@BrowsingBot:~$ sudo docker run -it --rm browsing-bot \
--action "$(cat action_file.json)" \
<website_name>
```

## Browse with login
The ```--login``` flag can also be specified to include the json representation of the login credentials.
```console
whyare@BrowsingBot:~$ sudo docker run -it --rm browsing-bot \
--login "$(cat login_file.json)" \
<website_name>
```

## Browse with actions and login
Both ```--login``` and ```--action``` flags can be specified to do both login and perform action
```console
whyare@BrowsingBot:~$ sudo docker run -it --rm browsing-bot \
--login "$(cat login_file.json)" \
--action "$(cat action_file.json)" \
<website_name>
```

## Test actions
Test login and page actions without browsing using the ```--test``` flag. The test flag accepts a string specifying the username to log in to, if no string is specified, then the bot will not login.

This command will login as user admin and perform the actions specified in ```action.json```.
```console
whyare@BrowsingBot:~$ sudo docker run -it --rm browsing-bot \
--action "$(cat action_file.json)" \
--login "$(cat login_file.json)" \
--test admin \
<website_name>
```

This command will only carry out the actions and will **not** attempt login
```console
whyare@BrowsingBot:~$ sudo docker run -it --rm browsing-bot \
--action "$(cat action_file.json)" \
--login "$(cat login_file.json)" \
<website_name> \
--test
```