#! /usr/bin/env python

"""main.py: Esgob NOC website"""

import os
from flask import Flask, render_template, send_from_directory, flash, request, redirect, url_for, g, Response
from flask.ext.cache import Cache
from ApiClient import ApiClient

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config.from_object(__name__)

# noc website


@app.before_request
def before_request():
    g.ac = ApiClient()
    g.ac.InternalKeyFromFile()
    g.ac.Endpoint("api.esgob.com", 80, False, "1.0")


@cache.cached(timeout=300)
@app.route('/')
def index():
    resp = g.ac.Call("internal/anycastnodes.list")
    if resp.success is False:
        return render_template('error_api.html'),501
    else:
        nodes = resp.data["anycastnodes"]
        return render_template('index.html', nodes=nodes)


@app.route('/peering')
def peering():
    return render_template('peering.html')


@app.route('/availability')
def availability():
    return render_template('availability.html')


@app.route('/looking_glass')
def looking_glass():
    return render_template('looking_glass_soon.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images/'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404


if __name__ == '__main__':
    app.debug = True
    app.run(port=5002)
