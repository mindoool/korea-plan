from application import app
from flask import render_template, request, redirect, url_for, session
import re
from application.models import filemanager
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

class ProfileForm(Form):
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


@app.route('/profile', methods=['POST', 'GET'])
def profile():
	user = usermanager.get_user_by_id(session['user_id'])
	form = ProfileForm(
		email = user.email,
		username = user.username,
		phone = user.phone,
		birthday = user.birthday,
		gender = user.gender)
	return render_template('profile.html', form=form, profile_image=user.profile_image)

@app.route("/info_revise_check/<int:id>", methods=['GET', 'POST'])
def info_revise_check(id):
	form = ProfileForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			if bool(re.match("[a-zA-Z0-9\.\_]+\@[a-zA-Z0-9-]+\.(com|net|ac.kr|co.kr)$", form.email.data)) == False:
				message = "Email no match"
				return render_template('profile.html', message=message, form=form)

			if bool(re.search("[a-zA-Z]+", form.password.data)) == False:
				message = "Password must have at least one Upper, Lower, Special Letter, and Number"
				return render_template('profile.html', message=message, form=form)
			elif bool(re.search("[0-9]+", form.password.data)) == False:
				message = "Password must have at least one Upper, Lower, Special Letter, and Number"
				return render_template('profile.html', message=message, form=form)
			elif bool(re.search("\W+", form.password.data)) == False:
				message = "Password must have at least one Upper, Lower, Special Letter, and Number"
				return render_template('profile.html', message=message, form=form)
			else:
				pass

			if form.password.data != form.password_check.data:
				message = "Password does not match"
				return render_template('profile.html', message=message, form=form)
			else:
				usermanager.revise_user(id, form.data)
				message = "Signed up successfully"
				get_user = usermanager.get_user_by_id(id)
				session['user_name']=get_user.username
				return redirect(url_for('wall', wall_id=get_user.id))
		else:
			return render_template('profile.html',form=form)
	else:
		return render_template('profile.html', form=form)



@app.route('/upload_image', methods=['POST'])
def upload_image():
	image_file=request.files['profile-image']

	filename = image_file.filename

	extension = filename.split('.')[-1]
	new_file_name = str(session['user_id'])+'.'+ extension

	directory = '/gs/korea-plan/profile/'

	# filepath = /gs/korea-plan/profile/5.jpg
	filepath = directory + new_file_name

	filemanager.save_file(image_file, filepath)

	usermanager.add_profile_image(session['user_id'], new_file_name)

	return redirect(url_for('profile'))

#http://korea-plan.appspot.com/image/progile/1
@app.route('/image/profile/<filename>')
def get_profile_image(filename):
	directory = '/gs/korea-plan/profile/'
	filepath = directory + filename
	return filemanager.read_file(filepath)