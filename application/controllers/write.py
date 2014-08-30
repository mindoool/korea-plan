from flask import request, session, redirect, url_for, render_template
from application import app
from application.models.schema import *
from application.models import postmanager


@app.route('/write', methods=['GET','POST'])
def write():
	if request.method == 'POST':
		data={}
		if "is_secret" in request.form:
			issecret=1
		else:
			issecret=0
		data["body"] = request.form['body']
		data["is_secret"] = issecret
		data["user_id"] = session['user_id']
		data["wall_id"] = session['wall_id']
		postmanager.write_post(data)
		return redirect(url_for('wall', wall_id=session['wall_id']))
	else:
		return render_template('write.html')