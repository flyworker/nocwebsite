#! /usr/bin/env python

"""main.py: Esgob NOC website"""

import os
from flask import Flask, render_template, send_from_directory, flash, request, redirect, url_for, g, Response
from flask.ext.cache import Cache
from ApiClient import ApiClient
from CommonConfig import CommonConfig

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config.from_object(__name__)

# noc website


@app.before_request
def before_request():
    g.cc = CommonConfig()
    g.ac = ApiClient(commonconfig=g.cc)


@cache.cached(timeout=300)
@app.route('/')
def index():
    resp = g.ac.Call("internal/anycastnodes.list")
    if resp.success is False:
        return render_template('error_api.html'), 501
    else:
        nodes = resp.data["anycastnodes"]
        return render_template('index.html', nodes=nodes)


@app.route('/peering')
def peering():
    return render_template('peering.html')


@app.route('/debug')
def debug():
    return render_template('debug.html')


@app.route('/availability')
def availability():
    return render_template('availability.html')


@app.route('/looking_glass')
def looking_glass():
    return render_template('looking_glass_soon.html')

@app.route('/secondary_dns')
def secondary_dns():
    return render_template('secondary_dns.html')


@app.route('/docs/api')
def docs_api():
    return render_template('docs_api.html')


@app.route('/docs/api/<resource>')
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
