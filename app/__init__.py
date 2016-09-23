#!flask/bin/python

from flask import Flask, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy

# global

title = 'Schedulee'

# create app

app = Flask(__name__)
app.config.from_object('config')

# create database

db = SQLAlchemy(app)

# import custom modules

from app import views, models, router, error

# define view routes

app.add_url_rule('/', '/index', methods = ['GET'], view_func = views.index)
app.add_url_rule('/adminpanel', methods=['GET', 'POST'], view_func = views.adminpanel)
app.add_url_rule('/groups/<int:groupId>', methods=['GET'], view_func = views.groups)
app.add_url_rule('/lessons/create/<int:groupId>', methods=['GET', 'POST'], view_func = views.createLesson)

# define rest api routes

app.add_url_rule('/api/groups', methods=['GET'], view_func = router.getGroups)
app.add_url_rule('/api/groups/<int:groupId>/lessons', methods=['GET'], view_func = router.getLessons)
app.add_url_rule('/api/lectors', methods=['GET'], view_func = router.getLectors)
app.add_url_rule('/api/lectors/<int:lectorId>', methods=['GET'], view_func = router.getLector)
