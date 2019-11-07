#!/usr/bin/python3

import sys
import datetime
from appUtils import *

commands = {"setPort": setPort,
            "openProxy": openProxy,
            "checkStatus": checkStatus,
            "runJob": runJob,
            "getShell": getShell,
            "getLogs": getLogs,
            "exit": sys.exit
            }


def printPrompt():
    ''' Use filename as prompt header'''
    currFileName = sys.argv[0]
    currentDT = datetime.datetime.now()
    '''print("{}:~$ ".format(currFileName), end="")'''
    print("{}:~$ ".format(currentDT), end="")


def parse(x):

    global commands

    try:
        splitted = x.split(" ")
        args = splitted[1:]
        try:
            func = commands[splitted[0]]
        except Exception as e:
            print(Exception("Command {} not found".
                            format(splitted[0])))
            raise Exception("Command {} not found".
                            format(splitted[0]))

        if (len(args) == 0):
            return func()
        elif (len(args) == 1):
            return func(args[0])
        else:
            return func(args)

    except Exception as e:
        raise (e)


def printSyntax(command):
    commands = {"setPort": "setPort <port for API to run on>",
                "openProxy": "openProxy",
                "checkStatus": "checkStatus",
                "runJob" : "runJob <client name> <worker name> <job name>",
                "getShell" : "getShell <client_name>",
                "getLogs": "getLogs <client name> <worker name>",
                "exit": "exit (exits the program)"
                }

    try:
        print(commands[command])
    except Exception as e:
        print("Command {} not a valid option".format(command))


def help(arg):

    global commands

    if (arg is False):
        print("List of Commands")
        print(list(commands.keys()))
        print("Type help <commandName> for help on syntax")
        print("Example - help changeName")
    else:
        printSyntax(arg)


def interactive():

    print("Type help to display available commands")
    print("Type \"exit\" to exit the program")

    while True:
        printPrompt()
        x = input().strip()

        if (not x):
            continue

        splitted = x.split()
        command = splitted[0]

        if command == "exit":
            break

        if command == "help":
            if (len(splitted) > 1):
                help(splitted[1])
            else:
                help(False)
        else:
            try:
                ret = parse(x)
                if (ret is not None):
                    print(ret)
            except Exception as e:
                print(e)
                print("Operation \"{}\" not successful\n"
                      .format(x))
                continue
