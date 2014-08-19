from application import app
from flask import render_template, request, redirect, url_for, session
from application.models.filemanager import *
from application.models.usermanager import *

@app.route('/profile')
def profile():
	user = get_user_by_id(session['user_id'])
	return render_template('profile.html', profile_image= user.profile_image)


@app.route('/upload_image', methods=['POST'])
def upload_image():
	image_file=request.files['profile-image']

	filename = image_file.filename

	extension = filename.split('.')[-1]
	new_file_name = str(session['user_id'])+'.'+ extension

	directory = '/gs/korea-plan/profile/'

	# filepath = /gs/korea-plan/profile/5.jpg
	filepath = directory + new_file_name

	save_file(image_file, filepath)

	add_profile_image(session['user_id'], new_file_name)

	return redirect(url_for('profile'))

#http://korea-plan.appspot.com/image/progile/1
@app.route('/image/profile/<filename>')
def get_profile_image(filename):
	directory = '/gs/korea-plan/profile/'
	filepath = directory + filename
	return read_file(filepath)