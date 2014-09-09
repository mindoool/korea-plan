from flask import request, session, redirect, url_for, render_template
from application import app
from application.models.schema import *
from application.models import usermanager
from application.models import postmanager
from sqlalchemy import desc


@app.route('/newsfeed', defaults={'newsfeed_id':0})
@app.route('/newsfeed/<int:newsfeed_id>')
def newsfeed(newsfeed_id):
    if not session['logged_in']:
        return redirect(url_for('login'))
    if newsfeed_id==0:
        newsfeed_id = session['user_id']
        
    session['newsfeed_id'] = newsfeed_id
    session['newsfeed_username']=usermanager.get_user(newsfeed_id).username

    return render_template('newsfeed.html')


@app.route('/newsfeed_ajax', methods=['POST', 'GET'])
def newsfeed_ajax():
    followee_list=[]
    followees = usermanager.get_user_by_id(session['user_id']).followees
    for followee in followees:
        followee_list.append(followee.followee_id)

    if 'number' in request.form:
        offset=int(request.form['number'])
        posts = postmanager.newsfeed_post(session['user_id'], followee_list).order_by(desc(Post.created_time))
        if posts.count() > offset+5 :
            readpost = posts.slice(offset,offset+5)
            return render_template("newsfeed_ajax.html", readpost=readpost)    
        elif offset < posts.count() < offset+5 :
            i = posts.count()-offset
            readpost = posts.slice(offset,i+offset)
            return render_template("newsfeed_ajax.html", readpost=readpost)
        else:
            return ''
    else:
        posts = postmanager.newsfeed_post(session['user_id'], followee_list).order_by(desc(Post.created_time))
        readpost=posts.slice(0,5)
        return render_template("newsfeed_ajax.html", readpost=readpost)