from globs import *
from werkzeug.utils import secure_filename
from flask import Flask, request, Response, send_file

import gzip, backend


app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return send_file('index.html')

@app.route('/api/<command>', methods=["OPTIONS"])
def api_opt_cors(command):
    resp = Response("")
    resp.headers["Access-Control-Allow-Origin"] = "https://netext.vercel.app/"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Max-Age"] = "86400"
    return resp
  
@app.route('/api/<command>', methods=["POST"])
def api(command):
    cmds = command.split("/")

    if cmds[0] == "follows":
        response = backend.get_follows(request)
    else:
        response = "Invalid Command"

    response = response.encode()

    response = Response(gzip.compress(response)) if response else ""

    response.headers["Access-Control-Allow-Origin"] = "https://netext.vercel.app/"
            
    return response