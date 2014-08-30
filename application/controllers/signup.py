from flask import request, render_template, redirect, url_for
from application import app
import re
import json
from application.models.schema import *
from application.models import usermanager
from flask.ext.wtf import Form
from wtforms import (
    StringField,
    PasswordField,
    RadioField,
    DateField
)
from wtforms import validators
from wtforms.fields.html5 import DateField

class SignForm(Form):
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
    password_check = PasswordField(
        u'Password check',
        [
            validators.data_required(message=u'please enter password'),
            validators.Length(min=8, max=20, message=None)
        ],
        description = {'placeholder': u'password check'}
    )
    username = StringField(
        u'Username',
        [
            validators.data_required(message=u'please enter your name')
        ],
        description = {'placeholder': u'username'}
    )
    gender = RadioField(
        u'Gender',
        choices=[('M','Male'),('F','Femal')]
    )
    phone = StringField(
        u'Phone',
        [
            validators.data_required(message=u'please your phone number')
        ],
        description = {'placeholder': u'phone number'}
    )
    birthday = DateField(
        u'Birthday:'
    )
#-*-coding:UTF-8 -*-


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        form = SignForm()
        if form.validate_on_submit():
            if bool(re.match("[a-zA-Z0-9\.\_]+\@[a-zA-Z0-9-]+\.(com|net|ac.kr|co.kr)$", form.email.data)) == False:
                message = "Email no match"
                return render_template('signup.html', message=message, form=form)
            
            if bool(re.search("[a-zA-Z]+", form.password.data)) == False:
                message = "Password must have at least one Upper, Lower, Special Letter, and Number"
                return render_template('signup.html', message=message, form=form)
            elif bool(re.search("[0-9]+", form.password.data)) == False:
                message = "Password must have at least one Upper, Lower, Special Letter, and Number"
                return render_template('signup.html', message=message, form=form)
            elif bool(re.search("\W+", form.password.data)) == False:
                message = "Password must have at least one Upper, Lower, Special Letter, and Number"
                return render_template('signup.html', message=message, form=form)
            else:
                pass
            
            if form.password.data != form.password_check.data:
                message = "Password does not match"
                return render_template('signup.html', message=message, form=form)
            else:
                usermanager.add_user(form.data)
                message = "Signed up successfully"
                return redirect(url_for('login'))
        else:
            return render_template('signup.html', form=form)
    else:
        form = SignForm()
        return render_template('signup.html', form=form)


@app.route("/email_check", methods=['POST'])
def email_check():
    form = SignForm()
    result = {}
    if usermanager.get_user_by_email2(form.email.data):
        result['message'] = "error"
    else:
        result['message'] = "ok"
    return json.dumps(result)


@app.route("/phone_check", methods=['POST'])
def phone_check():
    result={}
    if usermanager.get_user_by_phone(request.form['phone']):
        result['message'] = 'error'
    else:
        result['message'] = 'ok'
    return json.dumps(result)


@app.route("/info_revise/<int:id>")
def user_revise(id):
    get_user = usermanager.get_user_by_id(id)
    data= { 'email' : get_user.email,
    'username' : get_user.username,
    'phone' : get_user.phone
    }
    return render_template("signup.html", data=data)