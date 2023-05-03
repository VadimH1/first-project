import os
import json 
import jwt
from flask import Flask, Blueprint, request, render_template, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask import g, redirect, url_for
from models import Comments
from schemas import CommentsSchema
from db import db
from .user_api import login_required

import datetime

comment_urls = Blueprint("comment", __name__)

@comment_urls.route('/api/v1/create-comments/<int:post_id>', methods=['POST'])
@login_required
def create_comment(post_id):
    author_id = g.user_id
    post_id = post_id
    data = request.json
    text = data['text']
    created = datetime.datetime.utcnow()

    new_comm = Comments(
        text=text,
        created=created,
        author_id=author_id, post_id=post_id
    )
    
    db.session.add(new_comm)
    db.session.commit()

    comment_schema = CommentsSchema()

    return jsonify(comment_schema.dump(new_comm))


@comment_urls.route('/api/v1/update-comments/<int:comment_id>', methods=['PUT']) 
@login_required   
def update_comment(comment_id):
    data = request.json
    text = data['text']
    created = datetime.datetime.utcnow()

    comment = Comments.query.filter(
        Comments.id == comment_id,
        Comments.author_id == g.user_id
    ).first()

    if not comment:
        return {"Error": "This user hasn't comments"}
    
    comment.text = text
    comment.created = datetime.datetime.utcnow()

    db.session.commit()

    comment_schema = CommentsSchema()

    return jsonify(comment_schema.dump(comment))


@comment_urls.route('/api/v1/delete-comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comments(comment_id):
    author_id = g.user_id
    comment = Comments.query.filter(Comments.post_id==comment_id).all()

    if comment or not comment:
        for comments in comment:
            db.session.delete(comments)
            db.session.commit()

    return {"Status": "Comments deleted"}, 200


@comment_urls.route('/api/v1/delete-comment/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_one_comment(comment_id):
    author_id = g.user_id
    comment = Comments.query.filter(Comments.id==comment_id).first()

    if not comment:
        return {"Error": "Comment not found"}, 400
     
    db.session.delete(comment)
    db.session.commit()

    return {"Status": "One Comment deleted"}, 200


@comment_urls.route('/api/v1/comment/<int:comment_id>', methods=['GET'])
@login_required
def user_comment(comment_id):
    author_id = g.user_id
    comment = Comments.query.filter(Comments.id == comment_id).first()
    comment_schema = CommentsSchema()

    return jsonify(comment_schema.dump(comment))
