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

def runFile(filename):
    
    try:
        pid = os.fork()
    except Exception as e:
        print(e)
        raise(e)
    
    if (pid == 0): #run in child process
    
        commandToExecute = "kubectl apply -f %s" % filename
        params = commandToExecute.split(" ")
        
        try:
            os.execvp(params[0], params)
        except Exception as e:
            print(e)
            raise(e)
    
    else:
        #wait for child process to terminate
        os.waitpid(pid, 0)
    
