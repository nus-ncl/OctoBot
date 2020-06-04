import json
import os
import sys
import random

number = ((random.randint(1,2000)%17) * (random.randint(1,2000)%17)) % 5
while (number <= 0):
    number = (number + random.randint(1,4123) % 13) % 5

try:
    directory = str(os.getcwd()) + "/config/login" + str(number) + ".json"
    f = open(directory, "r")
    data = json.loads(f.read())
except:
    directory = str(os.getcwd()) + "/config/example-login.json"
    f = open(directory,"r")
    data = json.loads(f.read())

final_data = {"url": "http://10.10.0.112"}

def getCredentials():
    print("Reading from " + str(directory) + " ...")
    credentials = []
    number = 0
    for i in data:
        store = []
        if i == "url":
            continue
        else:
            information = data[i]
            if (number < 1):
            # if (information[2] == "false" and number < 1):
                credentials.append(information[0])
                credentials.append(information[1])
                # information[2] = "true"
                number += 1
            store.append(information[0])
            store.append(information[1])
            # store.append(information[2])
    final_data[i] = []
    final_data[i] = store
    with open(directory, "w") as fp:
        json.dump(final_data, fp)
    return credentials

def getUrl():
    return data["url"]
