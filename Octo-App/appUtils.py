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

# some random high value port, can change using setPort command
K8S_PORT = 8080

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

def parseStatusJson(dct):

    for pods in dct['items']:

        name = pods["metadata"]["name"]

        workers = pods["spec"]["containers"]

        print("Pod name: {}".format(name))

        for w in workers:
            print("Worker Name:{}".format(w["name"]))
            print("Worker Image:{}".format(w["image"]))
            print("Worker Job:{}\n".format(w["command"]))

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


def runJob(params):
    Pod = params[0]
    Worker = params[1]
    Jobs = params[2:]
    Command = ""

    for Job in Jobs:
        Command = Command + " " + str(Job)

    Command = "/snap/bin/microk8s.kubectl exec " + Pod + " " + Worker + " -- " + Command

    try:
        os.system(Command)
    except Exception as e:
        raise e

def getShell(param):
    Pod = param
    Command = "/snap/bin/microk8s.kubectl exec -it " + Pod + " -- /bin/bash"

    try:
        os.system(Command)
    except Exception as e:
        raise e