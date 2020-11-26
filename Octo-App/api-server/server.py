import flask
from flask import request, jsonify
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
@app.route('/api/v1/nodes', methods=['GET'])
def api_all():
    nodes = {}
    nodes['nodes'] = []
    response = get_node_api()
    for node in response['items']:
        name = node["metadata"]["name"]
        nodes['nodes'].append({
            'nodename': name
        })
    return jsonify(nodes)


app.run()
