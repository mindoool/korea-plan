from flask import request, session, redirect, url_for, render_template
from application import app
import json
from application.models.schema import *
from application.models import usermanager
from flask.ext.wtf import Form
from wtforms import (
    StringField,
    PasswordField
)
from wtforms import validators

class UserForm(Form):
    email = StringField(
        u'E-mail',
        [
            validators.data_required(message=u'please enter email'),
            validators.Email(message=u'use email form')
        ],
        description = {'placeholder': u'likelion@gmail.com'}
    )
    password = PasswordField(
        u'Password',
        [
            validators.data_required(message=u'please enter password'),
            validators.Length(min=8, max=20, message=None)
        ],
        description = {'placeholder': u'password'}
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = UserForm()
        if form.validate_on_submit():
            user = usermanager.login_check(form.email.data, form.password.data)
            if user.count() ==1:
                user=user.one()
                session['logged_in']=True
                session['email']=form.email.data
                session['user_id']=user.id
                session['user_name']=user.username
                return redirect(url_for('newsfeed',newsfeed_id=user.id))
            else:
                message = "wrong email or password"
                return render_template('login.html', form=form, message=message)
        else:
            return render_template('login.html', form=form)
    else:
        form = UserForm()
        return render_template('login.html', form=form)