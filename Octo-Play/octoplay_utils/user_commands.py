#!/usr/bin/python3

from octoplay_utils import utils
import parser
import io
import os
import sys
import time
import shlex
import requests
import yaml
from string import Template

'''
open template file to fill in values later
'''
file_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{file_path}/template.yaml", "r") as stream:
    z = yaml.safe_load(stream)


def get_api_version():
    """
    Returns API version in configuration
    """

    return z['apiVersion']


def get_name():
    """
    Returns the deployment name in configuration
    """
    return z['metadata']['name']


def set_name(name):
    """
    Sets the name of the deployment in configuration
    :param name: Name of deployment
    :return: print name
    """

    if type(name) != str and type(name) == list:
        name = name[0]

    z['metadata']['name'] = str(name)

    print(f'Name: {name}')


def get_bot_numbers():
    """
    Returns the number of bots in the configuration
    """
    return z['spec']['replicas']


def set_bot_numbers(number_of_bots):
    """
    Set the number of bots in the configuration
    :param number_of_bots: number of bots need to be created
    :return: replica value for number of bots/pods
    """

    z['spec']['replicas'] = int(number_of_bots)
    print(f"Bot Numbers: {z['spec']['replicas']}")


def get_executors():
    """
    List all the executors/containers in the configuration
    """

    print(f"Containers\t")
    executors = z['spec']['template']['spec']['containers']

    for i, c in enumerate(executors):
        command = c.get('command', '')
        if command:
            for count, com in enumerate(command):
                if len(com) > 50:
                    command[count] = com[:50] + "..."

        print(f"- Index\t\t:\t{i}")
        print(f"  Name\t\t:\t{c['name']}")
        print(f"  Image\t\t:\t{c['image']}")
        print(f"  Command\t:\t{command}")
        print(f"  ImgPullPolicy\t:\t{c['imagePullPolicy']}")


def add_executor(arguments):
    """
    Adds a executor/container to the configuration
    :param arguments: <name> <image> <command...>
    :return: executor/container spec added
    """

    # Splits the argument properly
    arguments = arguments.split(" ")

    # Parse the arguments
    name = arguments[0]
    image = arguments[1]
    command = " ".join(arguments[2:])

    # Obtain the existing executor/container information
    executors = z['spec']['template']['spec']['containers']

    # If there are no executor/containers to be copied as a template,
    # then create one on the spot now.
    if len(executors) > 0:
        # Make a copy of the template
        to_append = executors[0].copy()
    else:  # if there is no template to copy
        to_append = {}

    # Fill in the dictionary
    to_append['name'] = name
    to_append['image'] = image

    # Command has more handling
    if "$" in command:
        local_vars = parser.get_user_vars()
        t = Template(command)
        command = t.safe_substitute(local_vars)

    to_append['command'] = shlex.split(command)

    to_append['imagePullPolicy'] = "IfNotPresent"

    # Append the newly created executor/container
    executors.append(to_append)

    # Deletes all executors/containers with image None
    for i, c in enumerate(executors):
        if (c.get('image', None)) is None:
            del_executor(i)


def del_executor(index):
    """
    Deletes executor/container at index from configuration
    :param  index: Index of the executor/container in the configuration"
    :return: executor/container spec deleted
    """

    c = z['spec']['template']['spec']['containers']
    try:
        del c[int(index)]
    except Exception as e:
        raise e


def open_proxy(port=utils.K8S_PORT):
    """
    Configures kubernetes proxy to listen on the specified port
    :param port: Port to kubernetes proxy to listen to
    :return: success of failed
    """

    # Duplicates the program
    try:
        pid = os.fork()
    except Exception as e:
        raise e

    if pid == 0:  # This is the child process
        command = f"{utils.KUBECTL_CMD} proxy -p {port}"
        params = command.split(" ")

        try:
            os.execvp(params[0], params)
        except Exception as e:
            raise e

    else:  # Parent process
        # wait for child process to finish the kubectl command
        time.sleep(5)


def set_port(port):
    """
    Sets the port to communicate with the kubernetes proxy
    :param port: Port to communicate with the kubernetes API
    :return: Kubernetes proxy port
    """
    utils.K8S_PORT = int(port)


def load_file(filename):
    """
    Loads specified file into current configuration
    :param filename: configuration file
    :return: stream from the file
    """

    global z
    with open(filename) as stream:
        z = yaml.safe_load(stream)

    print(f'Successfully loaded file \'{filename}\'')


def write_file(filename):
    """
    Writes current configuration to the specified configuration file
    :param filename: configuration file
    :return: new file created
    """

    with io.open(filename, "w") as f:
        yaml.dump(z, f, default_flow_style=False,
                  explicit_start=True,
                  allow_unicode=True, sort_keys=False)
    f.close()


def run_file(params):
    """
    Applies the specified file in Kubernetes
    :param params: multiple configuration files
    :return:
    """

    try:
        pid = os.fork()
    except Exception as e:
        print(e)
        raise e

    # Split arguments
    params = shlex.split(params)

    if pid == 0:  # run in child process
        # push it to server iteratively
        for index in range(len(params)):
            utils.push_yaml_file(params[index])
        sys.exit(0)
    else:
        # wait for child process to terminate
        os.waitpid(pid, 0)


def patch_file(filename):
    """
    Patches the deployment using the given filename
    :param filename: configuration file
    :return: success or failed
    """

    # Obtain information from file
    with open(filename) as stream:
        deployment_content = yaml.safe_load(stream)
        deployment_name = deployment_content['metadata']['name']

    # Make API Call
    url = f'http://localhost:{utils.K8S_PORT}'\
          f'/apis/apps/v1/namespaces/default/deployments/{deployment_name}'
    headers = {'Content-Type': 'application/strategic-merge-patch+json'}
    resp = requests.patch(url, headers=headers, json=deployment_content)

    # Check status code
    if resp.status_code != 200:
        raise Exception(f"Error code {resp.status_code}: "
                        f"{resp.json().get('message', '')}")
    else:
        print(f'Successfully patched deployment \'{deployment_name}\'')


# Deletes deployment (Function name is like this
# because it fulfills the pep8 naming convention
def stop_file(filename):
    """
    Deletes the deployment specified in the filename
    :param filename: deployment file
    :return: success or failed
    """

    # Decide whether the argument is a filename or deployment_name
    try:
        with open(filename, 'r') as f:
            deployment_content = yaml.safe_load(f)
        deployment_name = deployment_content['metadata']['name']
    except FileNotFoundError as e:
        deployment_name = filename
    except Exception as e:
        raise Exception("An error occurred obtaining deployment name")

    api_url = f"http://localhost:{utils.K8S_PORT}"\
              f"/apis/apps/v1/namespaces/default/deployments/{deployment_name}"

    resp = requests.delete(api_url)

    # Gets status & status code
    status_code = resp.status_code
    json = resp.json()
    status = json.get('status', '')

    # Prints success or error message
    if status_code != 200 or status != 'Success':
        raise Exception(f"{json.get('message')}")
    else:
        print(f"Successfully deleted deployment \"{deployment_name}\"")


def check_status():
    """
    Checks status of the running bots
    :return: success or failed
    """

    try:
        pid = os.fork()
    except Exception as e:
        raise e

    if pid == 0:
        try:
            url = "http://localhost:{}/".format(utils.K8S_PORT) + \
                "api/v1/namespaces/default/pods"

            resp = requests.get(url)
            if resp.status_code != 200:
                # This means something went wrong.
                raise Exception(f"Error with code {str(resp.status_code)}: " +
                                resp.json().get('message'))

            else:
                print("Success with status code 200, \
                        parsing response...")

                utils.parse_status_json(resp.json())
        except Exception as e:
            print(e)
        finally:  # Please always exit the child process.
            sys.exit(0)
    else:
        os.waitpid(pid, 0)


def get_logs_by_command(args):
    """
    Finds the logs for a executor/container based on command
    :param args: <bot_name> <command>
        bot_name: name of the bot/pod
        command: command of the executor/container
    :return: log entries from executor/container in the bot/pod
    """

    # Split arguments
    args = shlex.split(args)

    # Get variables
    bot = args[0]
    command = " ".join(args[1:])

    # Get executor/container name by command
    executor = utils.get_executor_by_command(bot, command)
    executor_name = executor["name"]

    # Obtain the logs for that executor/container name
    return get_logs(f"{bot} {executor_name}")


def delete_bot(bot_name):
    """
    Deletes bot/pod using the specified name
    :param bot_name: name of the bot/pod to delete
    :return:
    """

    url = "http://localhost:{}/".format(utils.K8S_PORT) + \
          "api/v1/namespaces/default/pods/{}".format(bot_name)

    resp = requests.delete(url)

    if resp.status_code not in (200, 202):
        raise Exception(f"Error with code {str(resp.status_code)}: {resp.json().get('message', '')}")
    else:
        print("Successfully deleted pod".format(bot_name))


def get_logs(args):
    """
    Get logs for executors/containers
    :param args: <bot> <executor>
        bot: name of bot/pod
        executor: name of executor in the pod
    :return: success or failed response
    """

    # Split the string based on <space>
    args = shlex.split(args)

    # Get the variables from the arguments
    bot = args[0]
    executor = " ".join(args[1:]).strip()  # This is just for precautionary
    # measure, args[1] should ideally be enuf
    executor = executor if executor != '' else None

    url = "http://localhost:{}/".format(utils.K8S_PORT) + \
          "api/v1/namespaces/default/pods/" + \
          "{}/log".format(bot)

    # Figure out whether there is a executor/container or not
    param = {'container': executor} if executor is not None else None

    # Queries the API
    resp = requests.get(url, params=param)

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
    """
    Runs the specified command on a executor in a bot
    :param params: <bot> <executor> <command>
        bot: name of bot/pod
        executor: name of executor/container in the bot/pod
        command: name of command to run in the executor/container
    :return: failed or success response
    """

    # Make param a list
    params = params.split(' ')

    # Extract variables out
    bot = params[0]
    worker = params[1]
    job = " ".join(params[2:])   # Makes job back into a string

    # Get kubectl command
    command = f"{utils.KUBECTL_CMD} exec {bot} {worker} -- {job}"

    # Run the command
    try:
        os.system(command)
    except Exception as e:
        raise e


def get_shell(bot_name):
    """
    Get shell for the specified bot/pod
    :param bot_name: name of the bot
    :return: success or failed result
    """

    command = f"{utils.KUBECTL_CMD} exec -it {bot_name} -- /bin/bash"

    try:
        os.system(command)
    except Exception as e:
        raise e


def get_current_config():
    """
    Gets current configuration
    :return: configuration stream
    """

    print(f"API Version\t:\t{z['apiVersion']}")
    print(f"Name\t\t:\t{z['metadata']['name']}")
    print(f"Bot Numbers\t:\t{z['spec']['replicas']}")
    get_executors()


def exit():
    """
    Exit the program
    :return: system exit
    """
    sys.exit(0)
