import os
import json 
import jwt
from flask import Flask, Blueprint, request, render_template, session, jsonify, g
from models import Post
from schemas import PostSchema
from db import db
from .user_api import login_required
import datetime

post_urls = Blueprint("post", __name__)

@post_urls.route('/api/v1/create-post', methods=['POST'])
@login_required
def create_post():
    """Створення постів"""
    author_id = g.user_id   
    data = request.json
    title = data['title']
    body = data['body']
    image_id = data['image_id']
    created = datetime.datetime.utcnow()

    post = Post(author_id=author_id, title=title, body=body, created=datetime.datetime.utcnow(), image_id=image_id)
    db.session.add(post)
    db.session.commit()

    post_schema = PostSchema()
    
    return jsonify(post_schema.dump(post)) 


@post_urls.route('/api/v1/delete-post/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    """Видалення постів"""
    author_id = g.user_id
    post = Post.query.filter(Post.id == post_id, Post.author_id == g.user_id).first()
    # post = Post.query.get()
    db.session.delete(post)

    db.session.commit()
        
    return {"Status": "Deleted post"}, 200


@post_urls.route('/api/v1/update-post/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    """Оновлення постів"""
    author_id = g.user_id

    data = request.json
    title = data['title']
    body = data['body']
    image_id = data['image_id']
    created = datetime.datetime.utcnow()	

    post = Post.query.filter(Post.id == post_id, Post.author_id == g.user_id, image_id==image_id).first()
    
    if not post:
        return {"Error": "post not found"}, 400
    
    post.image_id = image_id
    post.title = title
    post.body = body
    post.created = datetime.datetime.utcnow()

    db.session.add(post)
    db.session.commit()

    post_schema = PostSchema()

    return jsonify(post_schema.dump(post)) 

 
@post_urls.route('/api/v1/posts', methods=['GET'])
@login_required
def get_user_post():
    """Список постів юзера"""
    post = Post.query.filter(Post.author_id==g.user_id).all()
    post_schema = PostSchema(many=True)
    # post_schema = PostSchema(many=True).dump(post)
    # return {"posts": post_schema}, 200

    return jsonify(post_schema.dump(post))


@post_urls.route('/api/v1/post/<int:post_id>', methods=['GET'])
@login_required
def user_post(post_id):
    """Виводимо пост користувача"""
    post = Post.query.filter(Post.id == post_id, Post.author_id == g.user_id).first()
    user_post_schema = PostSchema()
    
    return jsonify(user_post_schema.dump(post))
