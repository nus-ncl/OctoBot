import flask
from flask import request, jsonify, Flask
import json
import sys
sys.path.append('../Utils')
from appUtils import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API " \
           "for distant reading of science fiction novels.</p>"


# A route to return all of worker nodes.
@app.route('/api/v1/nodes/all', methods=['GET'])
def api_nodes():
    nodes = {}
    nodes['nodes'] = []
    response = get_node_api()
    for node in response['items']:
        name = node["metadata"]["name"]
        nodes['nodes'].append({
            'nodename': name
        })
    return jsonify(nodes)

# A route to return all of bots
@app.route('/api/v1/bots/all', methods=['GET'])
def api_bots():
    bots = {}
    bots['bots'] = []
    response = get_bot_api()

    for bot in response['items']:
        name = bot["metadata"]["name"]
        executors = bot["spec"]["containers"]
        for executor in executors:
            executor_name = executor["name"]
            executor_image = executor["image"]
            executor_task = executor["command"]
        node = bot["spec"]["nodeName"]
        bots['bots'].append({
            'name': name,
            'executor': executor_name,
            'image': executor_image,
            'task': executor_task,
            'node': node
        })

    return jsonify(bots)

# A route to return all of bots in specified node
@app.route('/api/v1/bot', methods=['GET'])
def api_bot_node():
    if 'nodeName' in request.args:
         nodename = str(request.args['nodeName'])
    else:
        return "Error: No node name field provided. Please specify a node name."
    bots = {}
    bots['bots'] = []
    response = get_bot_api()
    i = 1

    for bot in response['items']:
        name = bot["metadata"]["name"]
        node = bot["spec"]["nodeName"]
        if node == nodename:
            bots['bots'].append({
                'id': i,
                'name': name
            })
            i = i+1

    return jsonify(bots)


# A route to push job/task to specific bot/pod
@app.route('/api/v1/bot/run', methods=['POST'])
def api_run_task():
    data = json.loads(request.data)
    params = data["bot"] + " " + data["executor"] + " " + data["task"]
    params = str(params).split(" ")
    if params is None:
        return jsonify({"message": "task detail not found"})
    else:
        return jsonify({"message": run_job(params)})


app.run(host="0.0.0.0", port="8081", threaded=True)
