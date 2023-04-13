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
    """Додавання нового коментаря"""
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


@comment_urls.route('/api/v1/<comment_id>/update-comments/<user_id>', methods=['PUT']) 
@login_required   
def update_comment(comment_id, user_id):
    """Редагування(оновлення) коментарів"""
    data = request.json
    text = data['text']
    created = data['created']

    comment = Comments.query.filter(
        Comments.id == comment_id,
        Comments.author_id == user_id
    ).first()
    if not comment:
        return {"Error": "This user hasn't comments"}
    
    comment.text = text
    comment.created = datetime.datetime.now()

    db.session.commit()

    comment_schema = CommentsSchema(many=True)

    return jsonify(comment_schema.dump(comment))


@comment_urls.route('/api/v1/<user_id>/delete-comment', methods=['DELETE'])
@login_required
def delete_comment(user_id):
    """Видалення коментарів"""
    comment = Comments.query.get(user_id)
    db.session.delete(comment)
    db.session.commit()

    return {"Status": "Comment deleted"}
