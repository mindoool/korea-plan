from flask import session
from application import db
from schema import *


def write_comment(data):
    comment = Comment ( 
        body = data['body'],
        post_id = data['post_id'],
        user_id = data['user_id']
    )
    db.session.add(comment)
    db.session.commit() 

def read_comment_by_id(id):
    return Comment.query.filter(Comment.id == id).one()

def delete_comment(id):
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()

def get_by_post_id(post_id, is_desc = False) :
    post = postmanager.read_post_by_id(post_id)
    if is_desc : return post.comments.order_by(desc(Comment.created_time))
    else       : return post.comments.order_by(asc(Comment.created_time))
