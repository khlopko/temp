#!flask/bin/python

port = 8080

CSRF_ENABLED = True
SECRET_KEY = 'SecRetKeyForTesTinGgg.'

import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo')
