from flask import request, session, redirect, url_for, render_template
from application import app
from application.models.schema import *
from application.models import usermanager
from application.models import postmanager
from sqlalchemy import desc

@app.route('/wall', defaults={'wall_id':0})
@app.route('/wall/<int:wall_id>')
def wall(wall_id):
    if not session['logged_in']:
        return redirect(url_for('login'))
    if wall_id==0:
        wall_id = session['user_id']
        
    session['wall_id'] = wall_id
    session['wall_username']=usermanager.get_user(wall_id).username

    readpost = usermanager.get_user(wall_id).wall_posts.order_by(desc(Post.created_time))
    return render_template('wall.html', readpost=readpost)


@app.route('/wall_ajax', methods=['POST', 'GET'])
def wall_ajax():
    if 'number' in request.form:
        offset=int(request.form['number'])
        posts = usermanager.get_user(session['wall_id']).wall_posts.order_by(desc(Post.created_time))
        if posts.count() > offset+5 :
            readpost = posts.slice(offset,offset+5)
            return render_template("wall_ajax.html", readpost=readpost)    
        elif offset < posts.count() < offset+5 :
            i = posts.count()-offset
            readpost = posts.slice(offset,i+offset)
            return render_template("wall_ajax.html", readpost=readpost)
        else:
            return ''
    else:
        posts = usermanager.get_user(session['wall_id']).wall_posts.order_by(desc(Post.created_time))
        readpost=posts.slice(0,5)
        return render_template("wall_ajax.html", readpost=readpost)
        


    
@app.route('/delete/<int:id>')
def delete(id):
    post = postmanager.read_post_by_id(id)
    if (session['user_id']==post.user_id) or (session['user_id']==post.wall_id):
        delete_post(id)
    else:
        pass
    return redirect(url_for('wall', wall_id=post.wall_id))


@app.route('/post_revise/<int:id>')
def post_revise(id):
    post = postmanager.read_post_by_id(id)
    if session['user_id']==post.user_id:
        message = post.body
        message2 = post.id
        return render_template("post_revise.html",message=message, message2=message2)
    else:
        return redirect(url_for('wall', wall_id=post.wall_id))

@app.route('/post_revise_check/<int:id>', methods=['POST'])
def post_revise_check(id):
    post = postmanager.read_post_by_id(id)
    postmanager.revise_post(id, request.form)
    return redirect(url_for('wall', wall_id=post.wall_id))