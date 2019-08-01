#!/usr/bin/python3

import sys
from utils import *

commands = {"changeName": changeName,
            "updateClient": updateReplicas,
            "addWorker": addContainer,
            "getName": getName,
            "getWorkers": getContainers,
            "deleteWorker": deleteContainer,
            "writeToFile": writeToFile,
            "getClients": getReplicas,
            "checkStatus": checkStatus,
            "setPort": setPort,
            "openProxy": openProxy,
            "runFile": runFile,
            "checkStatus": checkStatus,
            "deletePod": deletePod,
            "getLogs": getLogs,
            "exit": sys.exit
            }


def printPrompt():
    ''' Use filename as prompt header'''
    currFileName = sys.argv[0]
    print("{}:~$ ".format(currFileName), end="")


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
    commands = {"changeName": "changeName <name>",
                "updateClient": "updateClient <# clients>",
                "addWorker": "addWorker <name> <image> <commands...>",
                "getName": "getName",
                "getWorkers": "getWorkers",
                "deleteWorker": "deleteContainer \
                                <container index from getContainers>",
                "writeToFile": "writeToFile <filename>",
                "getClients": "getClients",
                "runFile": "runFile <path to yaml config file>",
                "checkStatus": "Get status of the workers",
                "setPort": "setPort <port for API to run on>",
                "openProxy": "openProxy",
                "checkStatus": "checkStatus",
                "deletePod": "deletePod <pod name from checkStatus",
                "getLogs": "getLogs <pod name> <worker name>",
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
