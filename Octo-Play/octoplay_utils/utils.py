#!/usr/bin/python3

import yaml
import requests

# Global Variables
K8S_PORT = 12321
KUBECTL_CMD = 'kubectl'


def push_yaml_file(filename):
    try:
        u = "http://localhost:{}/".format(K8S_PORT) + \
            "apis/apps/v1/namespaces/default/deployments"

        print(u)
        with open(filename, "r") as stream:
            z = yaml.safe_load(stream)

        resp = requests.post(u, json=z)
        if resp.status_code != 201:
            # This means something went wrong.
            raise Exception(f"Error with code {str(resp.status_code)}: "
                            f"{resp.json().get('message')}")
        else:
            print("Success with status code 201")

    except Exception as e:
        print(e)


def parse_status_json(dct):
    for bots in dct['items']:
        # Get variables
        name = bots["metadata"]["name"]
        workers = bots["spec"]["containers"]

        # Format status
        is_terminating = bots['metadata']\
            .get('deletionTimestamp', None) is not None
        status = bots['status']['phase'] \
            if not is_terminating else "Terminating"

        # Calculate the number of executors/containers
        # in a bot/pod that is ready
        ready_count = 0
        total_count = 0
        for s in bots['status']['containerStatuses']:
            for k in s['state']:
                ready_count += 1 if k == 'running' else 0
            total_count += 1

        # Print output
        print("Bot name\t:\t{}".format(name))
        print("Status\t\t:\t{}".format(status))
        print("Ready\t\t:\t{}/{}".format(ready_count, total_count))

        for w in workers:
            # Cleanse cmd to not be so long
            cmd = w.get('command', '')
            for i, c in enumerate(cmd):
                if len(c) > 50:
                    cmd[i] = c[:50] + '...'

            print("Executor name\t:\t{}".format(w.get("name", None)))
            print("Executor image\t:\t{}".format(w.get("image", None)))
            print(f"Executor job\t:\t{cmd}\n")

        print("==================")


def get_executor_by_command(bot_name, command):
    url = f"http://localhost:{K8S_PORT}/" \
          f"api/v1/namespaces/default/pods/{bot_name}"

    resp = requests.get(url)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception(f"Error with code {str(resp.status_code)}: "
                        f"{resp.json().get('message', '')}")

    else:
        print("Success with status code 200, "
              "parsing response...")

        dct = resp.json()

        executors = dct["spec"]["containers"]

        for c in executors:
            executor_command = c['command']
            executor_command = " ".join(executor_command)

            if executor_command == command:
                return c

        raise Exception("Command not found in the bot")
