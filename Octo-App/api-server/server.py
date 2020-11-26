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
    return jsonify(get_node_api())


app.run()
