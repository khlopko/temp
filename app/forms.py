#!flask/bin/python

from flask_wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required


class LoginForm(Form):
    remember_me = BooleanField('remember_me', default=False)


class AddGroupForm(Form):
    title = TextField('group_title', validators=[Required()])
    course = TextField('group_course', validators=[Required()])


class AddLectorForm(Form):
    firstname = TextField('firstname', validators=[Required()])
    lastname = TextField('lastname', validators=[Required()])
    sorname = TextField('sorname', validators=[Required()])
