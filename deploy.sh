#!/bin/bash
scp main.py nat@wyntog.esgob.com:/var/www/esgobnoc/
scp ApiClient.py nat@wyntog.esgob.com:/var/www/esgobnoc/
scp ApiClient.pyc nat@wyntog.esgob.com:/var/www/esgobnoc/
rsync -arvuz templates/* nat@wyntog.esgob.com:/var/www/esgobnoc/templates/ --delete
rsync -arvuz static/* nat@wyntog.esgob.com:/var/www/esgobnoc/static/ --delete
scp esgobnoc.wsgi nat@wyntog.esgob.com:/var/www/esgobnoc/