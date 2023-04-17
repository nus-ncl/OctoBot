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
- **addExecutor** - name of the executor with specific working type (image) that required to execute job (command)
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
['currentConfig', 'getName', 'setName', 'getBotNumbers', 'setBotNumbers', 'getExecutors', 'addExecutor', 'deleteExecutor', 'openProxy', 'setPort', 'loadFile', 'writeFile', 'runFile', 'patchFile', 'stopFile', 'checkStatus', 'runJob', 'getShell', 'deletePod', 'getLogs', 'getLogsByCmd', 'exit']

List of functions
['read_file']
Type help <commandName> for help on syntax
Example - help getName

main.py:~$ setName test5
main.py:~$ setBotNumbers 2
main.py:~$ addExecutor worker-1 busybox ping 8.8.8.8
main.py:~$ writeFile test5.yaml
main.py:~$ runFile test5.yaml
http://localhost:8001/apis/apps/v1/namespaces/octobot/deployments
Success with status code 201
```

### Check the job execution in the bot
  
Check the job execution by using the same program prompt.
Use these following **command** to get different output:

```console
main.py:~$ checkStatus
Success with status code 200,                     parsing response...

Bot name    	:	test5-747b5c97cb-9827d
Status	    	:	Running
Ready           :	1/1
Executor Name	:	worker-1
Executor Image	:	busybox
Executor Job	:	['ping', '8.8.8.8']

==================
Bot name    	:	test5-747b5c97cb-cndl2
Status	    	:	Running
Ready	    	:	1/1
Executor Name	:	worker-1
Executor Image	:	busybox
Executor Job	:	['ping', '8.8.8.8']

==================

main.py:~$ getBotNumbers
2

main.py:~$ getExecutors
Containers	
- Index         :	0
  Name	    	:	worker-1
  Image	    	:	busybox
  Command   	:	ping 8.8.8.8
  ImgPullPolicy	:	IfNotPresent
```

### (Optional) Run Multiple Generation File

If there is lot of generation files that has been executed before, it can be 
re-executed together without required to fill the information one-by-one again.

Please use this command to run the file in batch:

```console
main.py:~$ runFile test5.yaml test6.yaml test7.yaml 
http://localhost:12321/apis/apps/v1/namespaces/octobot/deployments Success with status code 201
http://localhost:12321/apis/apps/v1/namespaces/octobot/deployments Success with status code 201
http://localhost:12321/apis/apps/v1/namespaces/octobot/deployments Success with status code 201
```