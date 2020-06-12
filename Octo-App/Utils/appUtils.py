#!/usr/bin/python3

import os
import time
import yaml
import io
import sys
import shlex

import requests

# some random high value port, can change using setPort command
K8S_PORT = 8080


'''
open template file to fill in values later
'''
file_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{file_path}/pod-template.yaml", "r") as stream:
    z = yaml.safe_load(stream)


def setBotNode(params):
    """<botname, nodename, imagename, command>
    Writes and apply current configuration
    botname: Affinity pod name
    nodename: worker node which bot will run
    imagename: image name need to be download
    command: default command to keep the bot alive"""

    botname = params[0]
    nodename = params[1]
    imagename = params[2]
    command = " ".join(params[3:])

    z['metadata']['name'] = str(botname)
    print(f'botName: {botname}')

    z['spec']['nodeName'] = str(nodename)
    print(f'nodeName: {nodename}')
    print(f'image: {imagename}')
    print(f'command: {command}')
    container = z['spec']['containers']

    # If there are no containers to be copied as a template, then create one on the spot now.
    if len(container) > 0:
        # Make a copy of the template
        to_append = container[0].copy()
    else:  # if there is no template to copy
        to_append = {}

    # Fill in the dictionary
    to_append['image'] = imagename
    to_append['command'] = shlex.split(command)
    container.append(to_append)

    filename = botname + ".yaml"

    # Deletes all containers with image None
    for i, c in enumerate(container):
        if (c.get('image', None)) is None:
            del_container(i)

    with io.open(filename, "w") as f:
        yaml.dump(z, f, default_flow_style=False,
                  explicit_start=True,
                  allow_unicode=True, sort_keys=False)
    f.close()

    try:
        pid = os.fork()
    except Exception as e:
        print(e)
        raise e

    if pid == 0:  # run in child process
        # push it to server
        push_pod_yaml_file(filename)

        sys.exit(0)
    else:
        # wait for child process to terminate
        os.waitpid(pid, 0)

def del_container(index):
    """<index>
    Deletes container at index from configuration

    index: Index of the container in the configuration"""

    c = z['spec']['containers']
    try:
        del c[int(index)]
    except Exception as e:
        raise e

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


def parseNodeJson(dct):
    for node in dct['items']:
        name = node["metadata"]["name"]
        print("Node name: {}".format(name))


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
        return "No logs for pod: {}, container :{}". \
            format(pod, container[0])

    elif (resp.status_code != 200):
        raise Exception("Error code {} when querying api\n" \
                        .format(resp.status_code) + \
                        "Error message: {}" \
                        .format(resp.json()['message']))
    return resp.text


def runJob(params):
    Pod = params[0]
    Worker = params[1]
    Jobs = params[2:]
    Command = ""

    for Job in Jobs:
        Command = Command + " " + str(Job)

    Command = "kubectl exec " + Pod + " " + Worker + " -- " + Command

    try:
        os.system(Command)
    except Exception as e:
        raise e


def getShell(param):
    Pod = param
    Command = "kubectl exec -it " + Pod + " -- /bin/bash"

    try:
        os.system(Command)
    except Exception as e:
        raise e


def getNodes():
    try:
        pid = os.fork()
    except Exception as e:
        raise (e)

    if (pid == 0):
        url = "http://localhost:{}/".format(K8S_PORT) + \
              "api/v1/nodes"
        resp = requests.get(url)

        if resp.status_code != 200:
            # This means something went wrong.
            raise Exception("Error with code " +
                            str(resp.status_code))
        else:
            print("Success with status code 200, \
                    parsing response...")

            parseNodeJson(resp.json())

    else:
        os.waitpid(pid, 0)


def push_pod_yaml_file(filename):
    try:
        u = "http://localhost:{}/".format(K8S_PORT) + \
            "api/v1/namespaces/default/pods"

        print(u)
        with open(filename, "r") as stream:
            z = yaml.safe_load(stream)

        resp = requests.post(u, json=z)
        if resp.status_code != 201:
            # This means something went wrong.
            raise Exception(f"Error with code {str(resp.status_code)}: "
                            f"{resp.json().get('message')}")
        else:
            print("Pod successfully in designated node")

    except Exception as e:
        print(e)


def deleteBot(pod_name):
    """<pod_name>
    Deletes pod using the specified name

    pod_name: Name of the pod to delete"""

    url = "http://localhost:{}/".format(K8S_PORT) + \
          "api/v1/namespaces/default/pods/{}".format(pod_name)

    resp = requests.delete(url)

    if resp.status_code not in (200, 202):
        raise Exception(f"Error with code {str(resp.status_code)}: "
                        f"{resp.json().get('message', '')}")
    else:
        print("Successfully deleted pod".format(pod_name))


def moveBotNode(params):
    """<botname, nodename>
    Move not to new node name
    botname : pod which one to delete and re-create
    nodename : new nodename for recreated pod"""

    try:
        deleteBot(params[0])
    except Exception as e:
        raise e

    try:
        url = "http://localhost:{}/".format(K8S_PORT) + \
              "api/v1/namespaces/default/pods/" + \
              "{}/status".format(params[0])
        resp = requests.get(url)

        while resp.status_code == 200:
            print("Pod {} still terminating".format(params[0]))
            time.sleep(1)
            resp = requests.get(url)

        setBotNode(params)

    except Exception as e:
        raise e
