from application import db
from schema import *

def add_follower(data):
	follow = Follow (
		follower_id = data['follower_id'],
		followee_id = data['followee_id']
	)
	db.session.add(follow)
	db.session.commit() 

def find_follow(follower_id, followee_id):
	return Follow.query.filter(Follow.follower_id==follower_id, Follow.followee_id==followee_id).count() != 0