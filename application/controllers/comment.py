from flask import request, session, redirect, url_for, flash
from application import app, db
from application.models.schema import *
from application.model import usermanage, postmanager, commentmanager

@app.route('/write_comment', methods=['GET','POST'])
def comment():
    if request.method == 'POST':
        data={}
        data['body'] = request.form['comment_body']
        data['post_id'] = session['post_id']
        data["user_id"] = session['user_id']
        commentmanager.write_comment(data)
    else:
        message= "You can't comment it"
    return redirect(url_for('read',id=session['post_id'], wall_id=session['wall_id']))


@app.route('/comment_delete/<int:id>')
def comment_delete(id):
    comment = read_comment_by_id(id)
    if session['user_id']==comment.user_id:
        delete_comment(id)
    else:
        flash("You can't delete it")
    return redirect(url_for('read',id=session['post_id'], wall_id=session['wall_id']))