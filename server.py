from globs import *
from werkzeug.utils import secure_filename
from flask import Flask, request, Response, send_file

import os, gzip
import gzip
import backend


app = Flask(__name__)


@app.route('/js/<name>', methods=["GET", "POST"])
def script(name):
    resp = send_file(os.path.join("./js/", secure_filename(name)))
    resp.headers["Access-Control-Allow-Origin"] = "https://netext.vercel.app/"
    
    return resp

@app.route('/', methods=["GET"])
def index():
    return ''

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

    response = Response(gzip.compress(response.encode()))

    response.headers["Access-Control-Allow-Origin"] = "https://ygo.helioho.st"
            
    return response