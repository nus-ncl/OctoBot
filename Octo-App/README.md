## Octo-App Preparation and User Guide

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
ncl@orchestrator:~/$ cd OctoBot/Octo-App
```
 
### Run Basic Octo-App Program
  
Call the program by using this command in order to get program prompt.
Insert the **required** parameters to run specific job or get the Shell for interactive execution:

- **runJob** - running specific task into specific bot
- **getShell** - accessing the shell (bash prompt)

The example of the running **ping** job are shown below: 
  
```console
ncl@controller-node:~/OctoBot/Octo-App$ python3 appMain.py 
Type help to display available commands
Type "exit" to exit the program
main.py:~$ help
List of Commands
['checkStatus', 'setPort', 'openProxy', 'runJob', 'getLogs', 'getShell', 'exit']
Type help <commandName> for help on syntax
Example - help setPort
2019-10-24 18:37:02.932048:~$ help runJob
runJob <client_name> <worker> <job>
2019-10-24 18:37:03.335678:~$ runJob busybox-d5f74c88b-5pzmf wk1 ping -c 3 8.8.8.8
ping 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: seq=0 ttl=50 time=3.178 ms
64 bytes from 8.8.8.8: seq=1 ttl=50 time=5.052 ms
64 bytes from 8.8.8.8: seq=2 ttl=50 time=3.812 ms

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip mon/avg/max = 3.178/4.014/5.052 ms
```

### (Optional) Octo-App Run "Moveable" or Dynamic Bot

This feature may required additional installation of NFS sharing in Octo-Pro 
component as shown [here](../Octo-Pro/README.md).

In order to run bot and move from one node to another node, please follow these
steps.

First, create bot in specific node with this following format `setBotNode 
<botname> <nodename> <image/worker type> <job/task>`
```console
setBotNode dynamic-bot-1 octobot-wk-1 nusncl1/healthcare-web-bot:latest python -u ./main.py -r patient
botname : dynamic-bot-1
nodename: octobot-wk-1
http://localhost:12321/api/v1/namespaces/octobot/pods
bot successfully in designated node
```

Second, move bot into specific node and may also change the task with this 
following format `setBotNode <moveBotNode> <nodename> <image/worker type> 
<job/task>`

```console
moveBotNode dynamic-bot-1 octobot-wk-2 nusncl1/healthcare-web-bot:latest python -u ./main.py -r patient
Successfully deleted bot
dynamic-bot-1 still terminating
....
....
botname : dynamic-bot-1
nodename: octobot-wk-2
http://localhost:12321/api/v1/namespaces/octobot/pods
bot successfully in designated node
```

### (Optional) Octo-App API Server

If there is requirement to allow access this Octo-App from third-party users or 
application, API server can be used. The detail how to enable and run API server
please check the detail documentation [here](api-server/README.md)