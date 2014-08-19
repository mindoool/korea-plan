from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from application import app, db
import json
from application.models.schema import *
from application.models.usermanager import *
from application.models.followmanager import *

@app.route('/member', methods=['GET', 'POST'])
def member():
    users = get_user_all()
    followers = get_user_by_id(session['user_id']).followers
    followees = get_user_by_id(session['user_id']).followees
    return render_template('member.html', users=users, followers=followers, followees=followees)


@app.route("/find_user", methods=['POST'])
def find_user():
    users = user_find(request.form['username'])
    return render_template("find_user.html", users=users)


@app.route("/following", methods=['POST'])
def following():
    if find_follow(session['user_id'], request.form['followee']):
        return ''
    else:
        data={}
        data["follower_id"] = session['user_id']
        data["followee_id"] = request.form['followee']
        add_follower(data)
        followee = get_user_by_id(request.form['followee'])
        return render_template("following.html", followee=followee)


@app.route("/followee", methods=['POST'])
def followee():
    users = user_find(request.form['username'])
    return render_template("find_user.html", users=users)