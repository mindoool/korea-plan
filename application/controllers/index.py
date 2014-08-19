#-*- coding:utf-8 -*-
from application import app
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from application.models.schema import *

@app.route('/')
@app.route('/layout')
def index() :
	if not 'logged_in' in session:
		return render_template('layout.html')
	else:
		return render_template('wall.html')


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