from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from application import app, db
from application.models.schema import *
from application.models.usermanager import *
from application.models.postmanager import *
from application.models.commentmanager import *
from sqlalchemy import asc

@app.route('/read', defaults={'id':0, 'message':None})
@app.route('/read/<int:wall_id>/<int:id>', methods=['GET','POST'], defaults={'message':None})
def read(id, wall_id, message):
    name = None
    if not session['logged_in']:
        return redirect(url_for('login'))
    if id==0:
        return redirect(url_for('wall', wall_id=post.user_id))
    if wall_id==0:
        wall_id = session['user_id']

    session['wall_id'] = wall_id
    session['wall_username']=get_user(wall_id).username
    session['post_id'] = id

    readpost=read_post_by_id(id)

    readcomment = read_post_by_id(id).comments.order_by(asc(Comment.created_time))
    message=message

    return render_template('read.html', readpost=readpost, readcomment=readcomment, message=message)