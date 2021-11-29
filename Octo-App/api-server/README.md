## Octo-App API Server Documentation

### Install and Run API Server

In order to install and run API server please use this script which will
automatically install Python [Flask](https://flask.palletsprojects.com/en/2.0.x/#)
and run it using default port `8081`

```console
ubuntu@octobot-o:~/OctoBot$ cd Octo-App/api-server
ubuntu@octobot-o:~/OctoBot/Octo-App/api-server$ ./start.sh
Collecting flask (from -r requirements.txt (line 1))
Using cached https://files.pythonhosted.org/packages/f2/28/2a03252dfb9ebf377f40fba6a7841b47083260bf8bd8e737b0c6952df83f/Flask-1.1.2-py2.py3-none-any.whl
...
...
Successfully installed Jinja2-2.11.2 MarkupSafe-1.1.1 Werkzeug-1.0.1 click-7.1.2 flask-1.1.2 itsdangerous-1.1.0
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:8081/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

### Test the API Calls from API Client

The API client can access with this following command and get this expected
output for getting all the available nodes:

```console
ubuntu@octobot-o:~$ curl http://127.0.0.1:8081/api/v1/nodes/all
{
  "nodes": [
    {
      "nodename": "k8s-master"
    }, 
    {
      "nodename": "octobot-wk-1"
    }, 
    {
      "nodename": "octobot-wk-2"
    }
  ]
}
```

The API client can access with this following command and get this expected
output for getting all running bots:

```console
ubuntu@octobot-o:~$ curl http://127.0.0.1:8081/api/v1/bots/all
{
  "bots": [
    {
      "executor": "worker-1", 
      "image": "busybox", 
      "name": "test-bot-1", 
      "node": "octobot-wk-1", 
      "task": [
        "ping", 
        "<ommitted>"
      ]
    }, 
...
...
...
```

The API client can access with this following command and get this expected
output for running specific job/task in specific executor and bot name:

```console
ubuntu@octobot-o:~$ curl -H "Content-type: application/json" -X POST http://localhost:8081/api/v1/bot/run -d '{"bot":"test-bot-1", "executor":"worker-1", "task":"ping -c 3 <ommitted>"}'
{
  "message": "Task ping -c 3 <ommited> is successfully run by worker-1 in bot test-bot-1"
}
```