from flask import request, render_template, redirect, url_for, session
from application import app
import re
import json
import os
from application.models.schema import *
from application.models.usermanager import *

#-*-coding:UTF-8 -*-


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    session.pop('number', None)
    message = None
    error = None
    if request.method == 'POST':
        if request.form['email'] == "" or request.form['password'] == "":
            message = "Fill All The Blanks!"
        elif bool(re.match("[a-zA-Z0-9\.\_]+\@[a-zA-Z0-9-]+\.(com|net|ac.kr|co.kr)$", request.form['email'])) == False:
            message = "Email no match"
        elif 8 <= len(request.form['password']) <= 20:          
            if bool(re.search("[a-zA-Z]+", request.form['password'])) == False:
                message = "Password must have at least one Upper, Lower, Special Letter, and Number"
            elif bool(re.search("[0-9]+", request.form['password'])) == False:
                message = "Password must have at least one Upper, Lower, Special Letter, and Number"
            elif bool(re.search("\W+", request.form['password'])) == False:
                message = "Password must have at least one Upper, Lower, Special Letter, and Number"
            else:
                if request.form['password_check'] == "":
                    message = "Password_check is empty"
                elif request.form['password_check'] != request.form['password']:
                    message = "Password does not match"
                else:
                    add_user(request.form)
                    message = "Signed up successfully"
                    return render_template('login.html', message=message)
        else:
            message = "The Password is Short!"
    else:
        return render_template('signup.html', message=message)


@app.route("/email_check", methods=['POST'])
def email_check():
    result = {}
    if get_user_by_email2(request.form['email']):
        result['message'] = "error"
    else:
        result['message'] = "ok"
    return json.dumps(result)


@app.route("/phone_check", methods=['POST'])
def phone_check():
    result={}
    if get_user_by_phone(request.form['phone']):
        result['message'] = 'error'
    else:
        result['message'] = 'ok'
    return json.dumps(result)


@app.route("/info_revise/<int:id>")
def user_revise(id):
    get_user = get_user_by_id(id)
    data= { 'email' : get_user.email,
    'username' : get_user.username,
    'phone' : get_user.phone
    }
    return render_template("signup.html", data=data)


@app.route("/info_revise_check/<int:id>", methods=['GET', 'POST'])
def user_revise_check(id):
    get_user = get_user_by_id(id)
    revise_user(id, request.form)
    session['user_name']=get_user.username
    return redirect(url_for('wall', wall_id=get_user.id))