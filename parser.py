#!/usr/bin/python3

import sys
from utils import *

def printPrompt():
    ''' Use filename as prompt header'''
    
    currFileName = sys.argv[0]
    print("{}:~$ ".format(currFileName), end="")
        
def parse(x):
    
    commands = {"changeApiVersion":changeApiVersion, \
            "changeName":changeName, \
            "updateClient":updateReplicas, \
            "addWorker":addContainer, \
            "updateSelector": updateSelector,\
            "getName":getName, \
            "getWorkers": getContainers, \
            "deleteWorker": deleteContainer, \
            "writeToFile": writeToFile, \
            "getApiVersion": getApiVersion, \
            "getSelector": getSelector, \
            "getClients": getReplicas, \
            "runFile": runFile}
    try:
        splitted = x.split(" ")
        args = splitted[1:]
        func = commands[splitted[0]]
        if (len(args) == 0):
            return func()
        elif (len(args) == 1):
            return func(args[0])
        else:
            return func(args)
            
    except Exception as e:
        print(e)
        raise (e)

def printSyntax(command):
    commands = {"changeApiVersion":"changeApiVersion <version>", \
        "changeName":"changeName <name>", \
        "updateClients": "updateClients <# clients>", \
        "addWorker": "addWorker <name> <image> <commands...>", \
        "getName": "getName (this prints the name of the current project)", \
        "getWorkers": "getWorkers (this lists out all the containers)", \
        "deleteWorker": "deleteContainer <container index from getContainers>", \
        "writeToFile": "writeToFile <filename>",\
        "getApiVersion": "getApiVersion",\
        "getSelector": "getSelector",\
        "updateSelector": "updateSelector <selector name>",\
        "getClients": "getClients (returns the number of clients)",\
        "runFile": "runFile <path to yaml config file>",\
        "exit": "exit (exits the program)"}
    
    try:
        print(commands[command])
    except:
        print("Command {} not a valid option".format(command))
            
def help(arg):
    commands = {"changeApiVersion":changeApiVersion, \
            "changeName":changeName, \
            "updateClient":updateReplicas, \
            "addWorker":addContainer, \
            "updateSelector": updateSelector,\
            "getName":getName, \
            "getWorkers": getContainers, \
            "deleteWorker": deleteContainer, \
            "writeToFile": writeToFile, \
            "getApiVersion": getApiVersion, \
            "getSelector": getSelector, \
            "getClients": getReplicas, \
            "runFile": runFile}
        

    
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
                print("Operation \"{}\" not successful\n".\
                    format(x))
                    
        

