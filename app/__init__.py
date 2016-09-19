#!flask/bin/python

from flask import Flask, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app import views, models, router, error

import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

loginManager = LoginManager()
loginManager.init_app(app)
openID = OpenID(app, os.path.join(basedir, 'tmp'))
