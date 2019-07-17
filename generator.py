import base64
import random
import string
import os
import sys
import yaml
import io

firstTimeAdding = True


with open("template.yaml", "r") as stream:
    try:
        z = yaml.safe_load(stream)
    except:
        pass

       
def changeApiVersion(api):
    z['apiVersion'] = api

def changeName(name):
    if (type(name) != str):
        if (type(name) == list):
            name = name[0]
    z['metadata']['name'] = str(name)
    
    
def updateReplicas(n):
    z['spec']['replicas'] = int(n)

def updateSelector(selector):
    z['spec']['selector']['matchlabels']['app'] = selector 
    

def addContainer(arg):
    c = z['spec']['template']['spec']['containers']
    toAppend = c[0].copy() 
    try:
        command = arg[2:]
        image = arg[1]
        name = arg[0]
        toAppend['name'] = name
        toAppend['image'] = image
        toAppend['command'] = list(command)
        c.append(toAppend)
    except Exception as e:
        print(e)
        print("syntax - addContainer <name> <image> <command>")
        print("eg - addContainer container1 ubuntu ping 1.1.1.1")
        raise(e)
    
    global firstTimeAdding
    if (firstTimeAdding):
        deleteContainer(0)
        firstTimeAdding = False 

def getContainers():
    return (z['spec']['template']['spec']['containers'])
    
def getName():
    return z['metadata']['name']

def getReplicas():
    return z['spec']['replicas'] 
    
def getApiVersion():
    return z['apiVersion']
    
def deleteContainer(index):
    c = z['spec']['template']['spec']['containers']
    try:
        del c[int(index)]
    except Exception as e:
        raise(e)
    
def getSelector():
    return z['spec']['selector']['matchlabels']['app']
    
def writeToFile(filename):

    with io.open(filename, "w") as f:
        yaml.dump(z, f, default_flow_style = False, \
        explicit_start=True,\
        allow_unicode = True, sort_keys=False)
        
    f.close()
    
    
def listener():
    x = input()
    while (x != 'exit'):
    
    
        try:
            ret = parse(x)
        except Exception as e:
            print(e)
        
        if (ret is not None):
            print(ret)
            
        x = input()
        
def parse(x):
    
    commands = {"changeApiVersion":changeApiVersion, \
            "changeName":changeName, \
            "updateReplicas":updateReplicas, \
            "addContainer":addContainer, \
            "updateSelector": updateSelector,\
            "getName":getName, \
            "getContainers": getContainers, \
            "deleteContainer": deleteContainer, \
            "writeToFile": writeToFile, \
            "getApiVersion": getApiVersion,\
            "getSelector": getSelector,\
            "getReplicas": getReplicas}
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
        "updateReplicas": "updateReplicas <# replicas>", \
        "addContainer": "addContainer <name> <image> <commands...>", \
        "getName": "getName (this prints the name of the current project)", \
        "getContainers": "getContainers (this lists out all the containers)", \
        "deleteContainer": "deleteContainer <container index from getContainers>", \
        "writeToFile": "writeToFile <filename>",\
        "getApiVersion": "getApiVersion",\
        "getSelector": "getSelector",\
        "updateSelector": "updateSelector <selector name>",\
        "getReplicas": "getReplicas (returns the number of replicas",\
        "exit": "exit (exits the program)"}
    
    try:
        print(commands[command])
    except:
        print("Command {} not a valid option".format(command))
            
def help(arg):
    commands = {"changeApiVersion":changeApiVersion, \
            "changeName":changeName, \
            "updateReplicas":updateReplicas, \
            "addContainer":addContainer, \
            "updateSelector": updateSelector,\
            "getName":getName, \
            "getContainers": getContainers, \
            "deleteContainer": deleteContainer, \
            "writeToFile": writeToFile, \
            "getApiVersion": getApiVersion,\
            "getSelector": getSelector,\
            "getReplicas": getReplicas}
        

    
    if (arg is False):
        print("List of Commands")
        print(list(commands.keys()))    
        print("Type help <commandName> for help on syntax")
        print("Example - help changeName")
    else:
        printSyntax(arg)
    
def interactive():
    
    print("Type help to display available commands")
    
    while True:
        x = input().strip() 
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
            except:
                print("Operation \"{}\" not successful\n".\
                    format(x))
                    
        
        print("\n")

   
   
    
if __name__ == "__main__":
    interactive()