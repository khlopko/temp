#!flask/bin/python

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

#
# Login.
#

class LoginForm(Form):
    remember_me = BooleanField('remember_me', default = False)

#
# Add group.
#

class AddGroupForm(Form):
	titleField = TextField('group_title', validators = [Required()])

#
# Add lector.
#

class AddLectorForm(Form):
	firstname = TextField('firstname', validators = [Required()])
	lastname = TextField('lastname', validators = [Required()])
	sorname = TextField('sorname', validators = [Required()])
