from flask import session
from application import db
from schema import *
from sqlalchemy import desc, or_
 
def write_post(data):
    post = Post ( 
        body = data['body'],
        is_secret = data['is_secret'],
        user_id = data['user_id'],
        wall_id = data['wall_id']
    )
    db.session.add(post)
    db.session.commit() 

def read_post_by_id(id):
    return Post.query.filter(Post.id == id).one()

def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()

def revise_post(id,data):
    post = Post.query.get(id)
    post.body=data['body']
    db.session.commit()

def newsfeed_post(user_id, followee_list):
    followee_list.append(user_id)
    return Post.query.filter((Post.user_id.in_(followee_list)) | (Post.wall_id.in_(followee_list)))
