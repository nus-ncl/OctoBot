## Octo-Play Preparation and User Guide

### Install Dependencies

This only work with Python version 3. Install with this following command:

```console
ncl@orchestrator:~$ sudo apt-get update
ncl@orchestrator:~$ sudo apt-get install python3 python3-pip
``` 

### Download the Source Code
 
Download the whole source of OctoBot software from the GitHub.
 
```console
ncl@orchestrator:~$ git clone https://github.com/nus-ncl/OctoBot
ncl@orchestrator:~$ cd OctoBot/Octo-Play
ncl@orchestrator:~/Octo-Play$ sudo pip3 install -r requirements.txt
```
 
### Run Octo-Play Program
  
Call the program by using this command in order to get program prompt.
Insert the **required** parameters:

- **setName** - name of the generation task
- **setBotNumbers** - how many bot is required to generate the activity
- **addWorker** - name of the worker with specific worker type (image) that required to execute job (command)
- **writeFile** - save the generation task into file
- **runFile** - run the file in order to start generation
- (Optional) **setPort** - in case if you listening different API port for OctoBot system

The example of the execution are shown below: 
  
```console
ncl@controller-node:~/OctoBot/Octo-Play$ python3 main.py 
Type "help" to display available commands
Type "exit" to exit the program
main.py:~$ help

List of commands
['currentConfig', 'getName', 'setName', 'getBotNumbers', 'setBotNumbers', 'getWorkers', 'addWorker', 'deleteWorker', 'openProxy', 'setPort', 'loadFile', 'writeFile', 'runFile', 'patchFile', 'stopFile', 'checkStatus', 'runJob', 'getShell', 'deletePod', 'getLogs', 'getLogsByCmd', 'exit']

List of functions
['read_file']
Type help <commandName> for help on syntax
Example - help getName

main.py:~$ setName test5
main.py:~$ setBotNumbers 2
main.py:~$ addWorker worker-1 busybox ping 8.8.8.8
main.py:~$ writeFile test5.yaml
main.py:~$ runFile test5.yaml
http://localhost:8001/apis/apps/v1/namespaces/default/deployments
Success with status code 201
```

### Check the job execution in the bot
  
Check the job execution by using the same program prompt.
Use these following **command** to get different output:

```console
main.py:~$ checkStatus
Success with status code 200,                     parsing response...

Pod name    	:	test5-747b5c97cb-9827d
Status	    	:	Running
Ready           :	1/1
Container Name	:	worker-1
Container Image	:	busybox
Container Job	:	['ping', '8.8.8.8']

==================
Pod name    	:	test5-747b5c97cb-cndl2
Status	    	:	Running
Ready	    	:	1/1
Container Name	:	worker-1
Container Image	:	busybox
Container Job	:	['ping', '8.8.8.8']

==================

main.py:~$ getBotNumbers
2

main.py:~$ getWorkers
Containers	
- Index         :	0
  Name	    	:	worker-1
  Image	    	:	busybox
  Command   	:	ping 8.8.8.8
  ImgPullPolicy	:	IfNotPresent
```
