# Tests
This section talks about the different types of unit testing for `healthcare-web-bot`. There are 2 kinds of tests done on the bot - tests with Firefox web interface UI and tests without Firefox web interface UI.

## Tests with Firefox web interface UI
```console
joelczk@OctoBot/Octo-Bot/<bot-name>:~$python3 TestUI.py
......
-------------------------------------------------------------------------
Ran 6 tests in X.XXXs
```

## Test without Firefox web interface UI
```console
joelczk@OctoBot/Octo-Bot/<bot-name>:~$python3 TestNoUI.py
......
-------------------------------------------------------------------------
Ran 6 tests in X.XXXs
```

By default, running tests using `test.sh` file would run both tests with Firefox web interface UI and without Firefox web interface UI