#-*- coding:utf-8 -*-
from application import app
from flask import session, redirect, url_for, render_template, flash
from application.models.schema import *

@app.route('/')
@app.route('/layout')
def index() :
	if not 'logged_in' in session:
		return render_template('layout.html')
	else:
		return redirect(url_for('newsfeed'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('admin', None)
    session.pop('wall_id', None)
    session.pop('wall_username', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404