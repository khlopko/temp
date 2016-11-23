#!flask/bin/python

# from migrate.versioning import api
from app import db
import os.path

db.create_all()
