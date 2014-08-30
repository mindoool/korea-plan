from flask import request, session, render_template
from application import app
from application.models.schema import *
from application.models import usermanager
from application.models import followmanager

@app.route('/member', methods=['GET', 'POST'])
def member():
    users = usermanager.get_user_all()
    followers = usermanager.get_user_by_id(session['user_id']).followers
    followees = usermanager.get_user_by_id(session['user_id']).followees
    return render_template('member.html', users=users, followers=followers, followees=followees)


@app.route("/find_user", methods=['POST'])
def find_user():
    users = usermanager.user_find(request.form['username'])
    return render_template("find_user.html", users=users)


@app.route("/following", methods=['POST'])
def following():
    if followmanager.find_follow(session['user_id'], request.form['followee']):
        return ''
    else:
        data={}
        data["follower_id"] = session['user_id']
        data["followee_id"] = request.form['followee']
        followmanager.add_follower(data)
        followee = usermanager.get_user_by_id(request.form['followee'])
        return render_template("following.html", followee=followee)


@app.route("/followee", methods=['POST'])
def followee():
    users = usermanager.user_find(request.form['username'])
    return render_template("find_user.html", users=users)