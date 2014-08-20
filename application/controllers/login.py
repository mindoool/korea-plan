from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from application import app
from application.models.schema import *
from application.models.usermanager import *

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('number', None)
    error = None
    if request.method == 'POST':
        if login_check(request.form['email_login'], request.form['password_login']):
            error = "Login Success"
            session['logged_in']=True
            session['email']=request.form['email_login']
            user=get_user_by_email(request.form['email_login'])
            session['user_id']=user.id
            session['user_name']=user.username
            return redirect(url_for('wall',wall_id=user.id))
        else:
            error = "No ID or Wrong password"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')