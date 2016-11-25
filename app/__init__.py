#!flask/bin/python

from flask import Flask, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# global

title = 'Schedulee'

# create app

app = Flask(__name__)
app.config.from_object('config')

# create database

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# import custom modules

from app import views, models, router, error

# define view routes

app.add_url_rule('/', '/index', methods=['GET'], view_func=views.index)
app.add_url_rule('/adminpanel', methods=['GET', 'POST'], view_func=views.adminpanel)
app.add_url_rule('/groups/<int:groupId>', methods=['GET'], view_func=views.groups)
app.add_url_rule('/lessons/create/<int:groupId>', methods=['GET', 'POST'], view_func=views.createLesson)

# define rest api routes

prefix = '/api/'

app.add_url_rule(prefix + 'groups', methods=['GET'], view_func=router.getGroups)
app.add_url_rule(prefix + 'groups/<int:groupId>/lessons', methods=['GET'], view_func=router.getLessons)
app.add_url_rule(prefix + 'lectors', methods=['GET'], view_func=router.getLectors)
app.add_url_rule(prefix + 'lectors/<int:lectorId>', methods=['GET'], view_func=router.getLector)
app.add_url_rule(prefix + 'bells', methods=['GET'], view_func=router.getBells)
app.add_url_rule(prefix + 'bells', methods=['POST'], view_func=router.createBell)
app.add_url_rule(prefix + 'bells/<int:id>', methods=['DELETE'], view_func=router.deleteBell)
