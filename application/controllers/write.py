from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from application import app, db
from application.models.schema import *
from application.models.postmanager import *
from application.models.usermanager import *
from application.models.commentmanager import *

@app.route('/write', methods=['GET','POST'])
def write():
	if request.method == 'POST':
		data={}
		data["body"] = request.form['body']
		data["is_secret"] = [0, 1]['is_secret' in request.form]
		data["user_id"] = session['user_id']
		data["wall_id"] = session['wall_id']
		write_post(data)
		return redirect(url_for('wall', wall_id=session['wall_id']))
	else:
		return render_template('write.html')