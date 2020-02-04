#!/usr/bin/python3

import yaml
import requests

# Global Variables
K8S_PORT = 12321


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
    for pods in dct['items']:
        # Get variables
        name = pods["metadata"]["name"]
        workers = pods["spec"]["containers"]

        # Format status
        is_terminating = pods['metadata'].get('deletionTimestamp', None) is not None
        status = pods['status']['phase'] if not is_terminating else "Terminating"

        # Calculate the number of containers in a pod that is ready
        ready_count = 0
        total_count = 0
        for s in pods['status']['containerStatuses']:
            for k in s['state']:
                ready_count += 1 if k == 'running' else 0
            total_count += 1

        # Print output
        print("Pod name\t:\t{}".format(name))
        print("Status\t\t:\t{}".format(status))
        print("Ready\t\t:\t{}/{}".format(ready_count, total_count))

        for w in workers:
            # Cleanse cmd to not be so long
            cmd = w.get('command', '')
            for i, c in enumerate(cmd):
                if len(c) > 50:
                    cmd[i] = c[:50] + '...'

            print("Container Name\t:\t{}".format(w.get("name", None)))
            print("Container Image\t:\t{}".format(w.get("image", None)))
            print(f"Container Job\t:\t{cmd}\n")

        print("==================")


def get_container_by_command(pod_name, command):
    url = f"http://localhost:{K8S_PORT}/" \
          f"api/v1/namespaces/default/pods/{pod_name}"

    resp = requests.get(url)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception(f"Error with code {str(resp.status_code)}: {resp.json().get('message', '')}")

    else:
        print("Success with status code 200, "
              "parsing response...")

        dct = resp.json()

        containers = dct["spec"]["containers"]

        for c in containers:
            container_command = c['command']
            container_command = " ".join(container_command)

            if container_command == command:
                return c

        raise Exception("Command not found in pod")
