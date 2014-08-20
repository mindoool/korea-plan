from application import db
from schema import *

def add_user(data):
	user = User ( email = data['email'],
		username = data['username'],
        gender = data['gender'],
        password = db.func.md5(data['password']),
        phone = data['phone'],
        birthday = data['birthday']
        )
	db.session.add(user)
	db.session.commit() 

def login_check(email, password):
	return User.query.filter(User.email == email, User.password == db.func.md5(password)).count() != 0

def get_user(wall_id):
	return User.query.filter(User.id == wall_id).one()

def get_user_by_email(email):
	return User.query.filter(User.email == email).one()

def is_email_duplicated(email) : 
    return User.query.filter(User.email == email).count() != 0

def get_user_by_id(id):
	return User.query.filter(User.id == id).one()

def get_user_by_phone(phone):
    return User.query.filter(User.phone == phone).count() != 0

def get_user_all():
    return User.query.all()

def revise_user(id,data):
    user = User.query.get(id)
    user.username=data['username']
    user.gender = data['gender']
    user.password = db.func.md5(data['password'])
    user.phone = data['phone']
    user.birthday = data['birthday']
    db.session.commit()

def add_profile_image(user_id, filename):
    user = get_user_by_id(user_id)
    user.profile_image=filename

    db.session.commit()

def user_find(term):
    return User.query.filter(User.username.like('%'+term+'%')).all()