#!flask/bin/python

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
from forms import LoginForm
from models import User, Role

#
# Index page.
#

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' }
    return render_template("index.html",
        title = 'Home',
        user = user)

#
# Login.
#

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/adminpanel')
    return render_template(
        'login.html',
        title = 'Sign In',
        form = form)

#
# Admin panel
#

@app.route('/adminpanel')
def adminpanel():
    return render_template('adminpanel.html')
