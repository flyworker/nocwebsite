#! /usr/bin/env python

"""main.py: Esgob NOC website"""

import os
from flask import Flask, render_template, send_from_directory, flash, request, redirect, url_for, g, Response, jsonify
from flask.ext.cache import Cache
from ApiClient import ApiClient
from CommonConfig import CommonConfig

app = Flask(__name__)
app.config.from_object(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# noc website


@app.before_request
def before_request():
    g.cc = CommonConfig()
    g.ac = ApiClient(commonconfig=g.cc)


def getnodesstate(nodes,state):
    matching = []
    for node in nodes:
        if node["state"] == state:
            matching.append(node)
    return matching

@app.route('/')
@cache.cached(timeout=30)
def index():
    resp = g.ac.Call("internal/anycastnodes.list")
    if resp.success is False:
        return render_template('error_api.html'), 501
    else:
        nodesall = resp.data["anycastnodes"]

	nodes = []
    nodes.extend(getnodesstate(nodesall,"maintenance"))
    nodes.extend(getnodesstate(nodesall,"live"))
    nodes.extend(getnodesstate(nodesall,"inprogress"))

    return render_template('index.html', nodes=nodes)


@app.route('/peering')
def peering():
    return render_template('peering.html')


@app.route('/status/anycast_instances')
@cache.cached(timeout=10)
def status_anycast_instances():
    resp = g.ac.Call("internal/anycastnodes.list")
    if resp.success is False:
        return render_template('error_api.html'), 501
    else:
        nodesall = resp.data["anycastnodes"]

	nodes = []
    nodes.extend(getnodesstate(nodesall,"maintenance"))
    nodes.extend(getnodesstate(nodesall,"live"))
    nodes.extend(getnodesstate(nodesall,"inprogress"))

    return render_template('status_anycast_instances.html', nodes=nodes)


@app.route('/debug')
def debug():
    return render_template('debug.html')


@app.route('/availability')
@cache.cached(timeout=30)
def availability():
    return render_template('availability.html')

@app.route('/looking_glass')
def looking_glass():
    return render_template('looking_glass_soon.html')

@app.route('/secondary_dns')
@cache.cached(timeout=30)
def secondary_dns():
    return render_template('secondary_dns.html')


@app.route('/docs/api')
@cache.cached(timeout=30)
def docs_api():
    return render_template('docs_api.html')


@app.route('/docs/docs_host_anycast_instance')
#@cache.cached(timeout=30)
def docs_host_anycast_instance():
    return render_template('docs_host_anycast_instance.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register/ajax/validate', methods=['POST'])
def register_ajax_validate():
    if "account" in request.form:
        field = "account"
    elif "email" in request.form:
        field = "email"
    else:
        return jsonify(valid=False)
    value = request.form[field]
    resp = g.ac.Call("internal/registration.validate.field?field=%s&val=%s" % (field, value))
    if resp.success is False:
        return jsonify(valid=False)
    return jsonify(valid=bool(resp.data["valid"]))


@app.route('/register/ajax/process', methods=['POST'])
def register_ajax_process():
    if "registration" not in request.json:
        return jsonify(success=False)
    reg = request.json["registration"]
    if "account" not in reg or "email" not in reg or "name" not in reg:
        return jsonify(success=False)
    registration = {
        "account": reg["account"].strip().lower(),
        "email": reg["email"].strip().lower(),
        "name": reg["name"].strip(),
        "ip": request.remote_addr,
        "browser": request.user_agent.string
    }
    resp = g.ac.Post("internal/registration.signup",registration)
    if resp.success is False:
        return jsonify(success=False)
    return jsonify(success=bool(resp.data["success"]))


@app.route('/docs/api/<resource>')
@cache.cached(timeout=30)
def docs_api_resource(resource):
    resource = resource.lower()
    try:
        return render_template("docs_api/%s.html" % (resource))
    except:
        return render_template('error_404.html'), 404


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images/'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404


if __name__ == '__main__':
    app.debug = True
    app.run(port=5002)
