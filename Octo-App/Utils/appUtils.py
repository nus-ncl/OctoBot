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


def load_file(filename):
    """<filename>
    Loads specified file/template into current configuration

    filename: Filename of the configuration file/template"""

    global z
    with open(filename) as stream:
        z = yaml.safe_load(stream)

    print(f'Successfully loaded file \'{filename}\'')


def set_bot_node(params):
    """<bot, node, image, command>
    Writes and apply current configuration

    bot: Affinity pod/bot name
    node: worker node which bot will run
    image: image name need to be download
    command: default command to keep the bot alive"""

    if len(params) < 3:
        raise Exception("setBotNode requires minimum 3 parameters. "
                        "Please use 'help setBotNode' for the detail")

    load_file("Utils/pod-template.yaml")

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
    executor = z['spec']['containers']

    # If there are no containers/executors to be copied as a template,
    # then create one on the spot now.

    if len(executor) > 0:
        # Make a copy of the template
        to_append = executor[0].copy()
    else:  # if there is no template to copy
        to_append = {}

    # Fill in the dictionary
    to_append['image'] = imagename
    to_append['command'] = shlex.split(command)
    executor.append(to_append)

    filename = botname + ".yaml"

    # Deletes all containers with image None
    for i, c in enumerate(executor):
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
    Deletes executor/container at index from configuration

    index: Index of the container in the configuration"""

    c = z['spec']['containers']
    try:
        del c[int(index)]
    except Exception as e:
        raise e


def open_proxy():
    """[port]
    Configures kubernetes proxy to listen on the specified port

    port: Port to kubernetes proxy to listen to"""

    try:
        pid = os.fork()
    except Exception as e:
        raise e

    if pid == 0:
        command = "kubectl proxy -p {}".format(K8S_PORT)
        params = command.split(" ")

        try:
            os.execvp(params[0], params)
        except Exception as e:
            raise e
    else:
        time.sleep(10)
        # let child sleep in background


def set_port(p):
    """<port>
    Sets the port to communicate with the kubernetes proxy

    port: Port to communicate with the kubernetes API"""

    global K8S_PORT
    K8S_PORT = int(p)


def parse_status_json(dct):
    """<dct>
    Parse the YAML config/template file or JSON response

    dct: content of the YAML/JSON file"""

    for bots in dct['items']:

        name = bots["metadata"]["name"]
        executors = bots["spec"]["containers"]
        node = bots["spec"]["nodeName"]
        print("Bot name: {}".format(name))
        print("Node name: {}".format(node))

        for w in executors:
            print("Executor name: {}".format(w["name"]))
            print("Image name: {}".format(w["image"]))
            print("Task name: {}\n".format(w["command"]))

        print("==================================")


def parse_status_by_node(dct, nodename):
    """<dct, nodename>
    Parse the YAML config/template file or JSON response

    dct: content of the YAML/JSON file
    nodename: specific node name"""

    print("List bots in the node: {}".format(nodename))
    print("============================")
    i = 1
    for bots in dct['items']:
        name = bots["metadata"]["name"]
        node = bots["spec"]["nodeName"]
        if node == nodename:
            print("%d | %s" % (i, name))
            i = i+1


def parse_status_by_job(dct, job):
    """<dct, job>
    Parse the YAML config/template file or JSON response

    dct: content of the YAML/JSON file
    job: job/task name"""

    print("List bots with this job: {}".format(job))
    print("========================================")
    i = 1

    for bots in dct['items']:
        name = bots["metadata"]["name"]
        executors = bots["spec"]["containers"]

        for w in executors:
            task = w["command"]
            if task == job:
                print("%d | %s" % (i, name))
                i = i+1

    print("========================================")


def parse_node_json(dct):
    """<dct>
    Get the Node name metadata from the YAML config/template file

    dct: content of the YAML file"""

    for node in dct['items']:
        name = node["metadata"]["name"]
        print("Node name: {}".format(name))


def get_bot_api():
    """
    Get status of the running bots/pods from REST API
    :return: JSON output from bots/pods list"""

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
        return resp.json()


def check_status():
    """
    Checks status of the running bots/pods
    :return: list of the bots/pods"""

    try:
        pid = os.fork()
    except Exception as e:
        raise e

    if pid == 0:
        parse_status_json(get_bot_api())
    else:
        os.waitpid(pid, 0)


def get_bot_by_node(nodename):
    """
    List of the running bots/pods based on node name

    nodename: sepcific node name to query"""

    try:
        pid = os.fork()
    except Exception as e:
        raise e

    if pid == 0:
        parse_status_by_node(get_bot_api(), nodename)
    else:
        os.waitpid(pid, 0)


def get_bot_by_job(jobname):
    """
    List of the running bots/pods based on job/task name

    jobname: specific job/task name to query"""

    try:
        pid = os.fork()
    except Exception as e:
        raise e

    if pid == 0:
        parse_status_by_job(get_bot_api(), jobname)
    else:
        os.waitpid(pid, 0)


def get_logs(params):
    """<bot, worker>
    Get logs for bots or specific executor name

    bot: Name of bot/pod
    worker: Name of executor/container in the bot/pod"""

    params = shlex.split(params)
    bot = params[0]

    try:
        executor = params[1]
    except Exception as e:
        executor = False

    url = "http://localhost:{}/".format(K8S_PORT) + \
          "api/v1/namespaces/default/pods/" + \
          "{}/log".format(bot)

    if executor:
        param = {'container': executor}
    else:
        param = None

    try:
        if param:
            resp = requests.get(url, params=param)
        else:
            resp = requests.get(url)
    except Exception as e:
        raise e

    if resp.status_code == 204:
        return "No logs for bot: {}, executor :{}". \
            format(bot, executor[0])

    elif resp.status_code != 200:
        raise Exception("Error code {} when querying api\n"
                        .format(resp.status_code) +
                        "Error message: {}"
                        .format(resp.json()['message']))
    return resp.text


def run_job(params):
    """<bot> <executor> <command>
    Runs the specified task/job command on a executor/container in a bot/pod

    bot: Name of bot/pod
    executor: Name of executor/container in the bot/pod
    command: Name of task/job command to be ran in the executor/container"""

    bot = params[0]
    executor = params[1]
    jobs = " ".join(params[2:])

    command = "kubectl exec -i -t " + bot + " --container " \
              + executor + " -- " + jobs

    try:
        os.system(command)
        message = "Task " + jobs + " is successfully run by " + executor \
                  + " in bot " + bot
    except Exception as e:
        raise e
        message = "Task can't be executed"

    return message


def get_shell(bot):
    """<bot>
    Gets shell for the specified pod

    bot: Name of bot/pod"""

    command = "kubectl exec -it " + bot + " -- /bin/bash"

    try:
        os.system(command)
    except Exception as e:
        raise e


def get_node_api():
    """
    Gets all available worker nodes for bot/pod
    """

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

        return resp.json()


def get_nodes():
    """
    Gets all available worker nodes for bot/pod
    :return: list of the worker nodes
    """

    try:
        pid = os.fork()
    except Exception as e:
        raise e

    if pid == 0:
        parse_node_json(get_node_api())
    else:
        os.waitpid(pid, 0)


def push_pod_yaml_file(filename):
    """<filename>
    Deploy bot/pod base on the YAML file

    filename: Name of YAML file"""

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
            print("Bot successfully in designated node")

    except Exception as e:
        print(e)


def delete_bot(bot):
    """<bot>
    Deletes bot/pod using the specified name

    bot: Name of the bot/pod to delete"""

    url = "http://localhost:{}/".format(K8S_PORT) + \
          "api/v1/namespaces/default/pods/{}".format(bot)

    resp = requests.delete(url)

    if resp.status_code not in (200, 202):
        raise Exception(f"Error with code {str(resp.status_code)}: "
                        f"{resp.json().get('message', '')}")
    else:
        print("Successfully deleted pod".format(bot))


def move_bot_to_node(params):
    """<bot, node>
    Move not to new node

    bot : bot/pod which one to delete and re-create
    node : new node name for recreate bot/pod"""

    try:
        delete_bot(params[0])
    except Exception as e:
        raise e

    try:
        url = "http://localhost:{}/".format(K8S_PORT) + \
              "api/v1/namespaces/default/pods/" + \
              "{}/status".format(params[0])
        resp = requests.get(url)

        while resp.status_code == 200:
            print("Bot is {} still terminating".format(params[0]))
            time.sleep(5)
            resp = requests.get(url)

        if len(params) < 4:
            bot_config = params[0] + ".yaml"
            load_file(bot_config)
            z['spec']['nodeName'] = str(params[1])

            with io.open(bot_config, "w") as f:
                yaml.dump(z, f, default_flow_style=False,
                          explicit_start=True,
                          allow_unicode=True, sort_keys=False)
            f.close()
            push_pod_yaml_file(bot_config)
        else:
            set_bot_node(params)

    except Exception as e:
        raise e


def exit():
    """
    Exits the program"""
    sys.exit(0)