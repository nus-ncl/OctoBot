## Octo-Play Preparation and User Guide

### Install Dependencies

This only work with Python version 3. Install with this following command:

```console
ncl@orchestrator:~/$ sudo apt-get update
ncl@orchestrator:~/$ sudo apt-get install python3
``` 

### Download the Source Code
 
Download the whole source of OctoBot software from the GitHub.
 
```console
ncl@orchestrator:~/$ git clone https://github.com/nus-ncl/OctoBot
ncl@orchestrator:~/$ cd OctoBot/Octo-Play
```
 
### Run Octo-Play Program
  
Call the program by using this command in order to get program prompt.
Insert the **required** parameters:

- **changeName** - name of the generation task
- **updateClient** - how many client to generate the traffic
- **addWorker** - name of the worker with specific worker type (image) that required to execute job (command)
- **writeToFile** - save the generation task into file
- **runFile** - run the file in order to start generation
- (Optional) **setPort** - in case if you listening different API port for OctoBot system

The example of the execution are shown below: 
  
```console
ncl@controller-node:~/OctoBot/Octo-Play$ python3 main.py 
Type help to display available commands
Type "exit" to exit the program
main.py:~$ help
List of Commands
['changeName', 'updateClient', 'addWorker', 'getName', 'getWorkers', 'deleteWorker', 'writeToFile', 'getClients', 'checkStatus', 'setPort', 'openProxy', 'runFile', 'deleteClient', 'getLogs', 'getLogsByCommand', 'exit']
Type help <commandName> for help on syntax
Example - help changeName
main.py:~$ changeName test5
main.py:~$ updateClient 2
main.py:~$ addWorker worker-1 ariscahyadi/web-browsing-bot:latest python -u /main.py https://ncl.sg 0
main.py:~$ writeToFile test5.yaml
main.py:~$ setPort 8001
main.py:~$ runFile test5.yaml
http://localhost:8001/apis/apps/v1/namespaces/default/deployments
Success with status code 201
```

### Check the traffic generation
  
Check the traffic generation by using the same program prompt.
Use these following **command** to get different output:

```console
main.py:~$ checkStatus
Success with status code 200,                     parsing response...

Pod name: test5-59b784b5d5-5tfwl
Worker Name:worker-1
Worker Image:ariscahyadi/web-browsing-bot:latest
Worker Job:['python', '-u', './main.py', 'https://ncl.sg', '0']
==================
Pod name: test5-59b784b5d5-r68nm
Worker Name:worker-1
Worker Image:ariscahyadi/web-browsing-bot:latest
Worker Job:['python', '-u', './main.py', 'https://ncl.sg', '0']
==================

main.py:~$ getClients
2

main.py:~$ getWorkers
[{'name': 'worker-1', 'image': 'ariscahyadi/web-browsing-bot:latest', 'command': ['python', '-u', './main.py', 'https://ncl.sg', '0'], 'imagePullPolicy': 'IfNotPresent'}]
```