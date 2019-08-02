#!/usr/bin/python3

import base64
import random
import string
import os
import sys
import yaml
import io
import time
import requests

firstTimeAdding = True

# some random high value port, can change using setPort command
K8S_PORT = 12321

'''
open template file to fill in values later
'''
with open("template.yaml", "r") as stream:
    z = yaml.safe_load(stream)


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
        yaml.dump(z, f, default_flow_style=False,
                  explicit_start=True,
                  allow_unicode=True, sort_keys=False)

    f.close()


def openProxy():

    try:
        pid = os.fork()
    except Exception as e:
        raise (e)

    if (pid == 0):
        command = "kubectl proxy -p {}".format(K8S_PORT)
        params = command.split(" ")

        try:
            os.execvp(params[0], params)
        except Exception as e:
            raise e

    else:

        time.sleep(10)
        # let child sleep in background


def setPort(p):

    global K8S_PORT
    K8S_PORT = int(p)


def pushYamlFile(filename):
    try:

        u = "http://localhost:{}/".format(K8S_PORT) +\
            "apis/apps/v1/namespaces/default/deployments"

        print(u)
        with open(filename, "r") as stream:
            z = yaml.safe_load(stream)

        resp = requests.post(u, json=z)
        if resp.status_code != 201:
            # This means something went wrong.
            raise Exception("Error with code " +
                            str(resp.status_code))
        else:
            print("Success with status code 201")

    except Exception as e:
        print(e)


def runFile(filename):

    try:
        pid = os.fork()
    except Exception as e:
        print(e)
        raise(e)

    if (pid == 0):  # run in child process

        # push it to server
        pushYamlFile(filename)

    else:

        # wait for child process to terminate
        os.waitpid(pid, 0)


def parseStatusJson(dct):

    for pods in dct['items']:

        name = pods["metadata"]["name"]

        workers = pods["spec"]["containers"]

        print("Pod name: {}".format(name))

        for w in workers:
            print("Worker Name:{}".format(w["name"]))
            print("Worker Image:{}".format(w["image"]))
            print("Worker command:{}\n".format(w["command"]))

        print("==================")


def checkStatus():
    try:
        pid = os.fork()
    except Exception as e:
        raise (e)

    if (pid == 0):

        url = "http://localhost:{}/".format(K8S_PORT) + \
            "api/v1/namespaces/default/pods"

        resp = requests.get(url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise Exception("Error with code " +
                            str(resp.status_code))

        else:
            print("Success with status code 200, \
                    parsing response...")

            parseStatusJson(resp.json())

    else:
        os.waitpid(pid, 0)


def deletePod(podName):

    url = "http://localhost:{}/".format(K8S_PORT) + \
            "api/v1/namespaces/default/pods/{}".format(podName)

    try:

        resp = requests.delete(url)

        if (resp.status_code not in (200, 202)):
            raise Exception("Error with code " +
                            str(resp.status_code))
        else:
            print("Successfully deleted pod".format(podName))
    except Exception as e:
        raise e

def getWorkerNameByCommand(pod, command):

    url = "http://localhost:{}/".format(K8S_PORT) + \
        "api/v1/namespaces/default/pods"

    resp = requests.get(url)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception("Error with code " +
                        str(resp.status_code))

    else:
        print("Success with status code 200, \
                parsing response...")

        dct = resp.json()
        
        foundPod = False
        
        for pods in dct['items']:
        
            name = pods["metadata"]["name"]
            if (name == pod):
                foundPod = pods
                break
        
        if (foundPod):
            workers = foundPod["spec"]["containers"]
            
            myCommand = command
            for w in workers:
                
                workerCommand = w['command']
                if (workerCommand == myCommand):
                    return w
            
            raise Exception("Command not found in pod")
            
        else:
            raise Exception("Pod not found")

def getLogsByCommand(param): 
    
    pod = param[0]
    command = param[1:]
    
    worker = getWorkerNameByCommand(pod, command)
    workerName = worker["name"]
    
    return getLogs([pod, workerName])
                                                                                                                                                                                                              
def getLogs(params):
    
    pod = params[0]
    
    try:
        container = params[1]
    except Exception as e:
        container = False
    
    url = "http://localhost:{}/".format(K8S_PORT) + \
            "api/v1/namespaces/default/pods/" + \
            "{}/log".format(pod)
    
    if (container):
        param = {'container': container}
    else:
        param = None
    
    try:
        if (param):
            resp = requests.get(url, params = param)
        else:
            resp = requests.get(url)
    except Exception as e:
        raise(e)
    
    if (resp.status_code == 204):
        return "No logs for pod: {}, container :{}".\
                            format(pod, container[0])
    
    elif (resp.status_code != 200):
        raise Exception("Error code {} when querying api\n"\
                            .format(resp.status_code) +\
                            "Error message: {}"\
                            .format(resp.json()['message']))
        
    return resp.text
    
    
