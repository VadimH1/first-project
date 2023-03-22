
import os
import json #jsonify ?
import jwt
from flask import Flask, Blueprint, request, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask import g, redirect, url_for
from .models import Post, User, Comments, Upload
from .db import db
from werkzeug.utils import secure_filename
from .config import SECRET_KEY
import datetime

hello_urls = Blueprint("sync", __name__)

# @hello_urls.route("/", methods=['GET', 'POST'])
# def index():
#     if request.method == "GET":
#         print("Ми викликали GET")
#         return render_template("index.html")

#     if request.method == "POST":
#         print("Ми викликали POST")
#         form = request.form # ImmutableMultiDict([('fname', 'Andy'), ('lname', 'KOOccccc')])
#         # import pdb; pdb.set_trace()
#         _data = {
#             "fname": form["fname"],
#             "lname": form["lname"]
#         }
#         return render_template("index.html", income_form_data=_data)

# Working code
@hello_urls.route("/api/v1/register-user", methods=['POST'])
def register_user_api():
    data = request.json
    phone_number = data["phone_number"]
    first_name = data["first_name"]
    second_name = data["second_name"]
    password = data["password"]
    
    user = User(phone_number, first_name, second_name, password)
    db.session.add(user)
    db.session.commit()

    return {}, 200


def login_required(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
        user_id = int(kwargs.get("user_id"))
         
        access_token = request.headers.get("Authorization")
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        token_user_id = payload["user_id"] 
              
        if not token_user_id:
            return {"error": "Користувач не авторизований"}, 403
            
        user = User.query.filter(User.id == token_user_id).first()

        if not user:
            return {"error": f"Користувач не існує {user_id}"}, 404

        return f(*args, **kwargs)
    return _wrapper

@hello_urls.route("/api/v1/login", methods=['POST'])
def login_api():
    data = request.json # Analog

    income_phone_number = data.get("phone_number") # Данні з запиту
    income_password = data.get("password") # Данні з запиту

    if not income_phone_number or not income_password:
        return "", 401
        
    user = User.query.filter(User.phone_number == income_phone_number).one()
    
    if not user:
        return {"error": f"Користувач не існує з телефоном {income_phone_number}"}, 404

    token_data = {"user_id": user.id}
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm='HS256') 
    return {"access_token": access_token}, 200

# Working code
@hello_urls.route("/api/v1/user-info/<user_id>", methods=['GET'])
@login_required
def user_info_api(user_id):
    user = User.query.filter(User.id == user_id).first()
    if not user:
        return {"Неверный логин или пароль"}, 400
    return {"info": user.full_name()}, 200
    
# Working code    
@hello_urls.route('/api/v1/create-post/<user_id>', methods=['POST'])
@login_required
def create_post(user_id):
    """Створення постів"""
    data = request.json
    title = data['title']
    body = data['body']
    created = data['created']	
    author_id = None

    post = Post(title=title, body=body, created=datetime.datetime.now(), author_id=user_id)
    db.session.add(post)
    db.session.commit()

    return {"Status": "Created post"}, 200
    
# Working code    
@hello_urls.route('/api/v1/delete-post/<user_id>', methods=['DELETE'])
@login_required
def delete_post(user_id):
    """Видалення постів"""
    post = Post.query.get(user_id)
    db.session.delete(post)
    db.session.commit()
        
    return {"Status": "Deleted post"}, 200

# Working code
@hello_urls.route('/api/v1/update-post/<post_id>/<user_id>', methods=['PUT'])
@login_required
def update_post(post_id, user_id):
    """Оновлення постів"""
    data = request.json
    title = data['title']
    body = data['body']
    created = data['created']	
    author_id = None  # author_id = g.request.user_id

    post = Post.query.filter(Post.id == post_id, Post.author_id == user_id).first()
    if not post:
        return {"Error": "post not found"}, 400
    
    post.title = title
    post.body = body
    post.created = datetime.datetime.now()

    db.session.add(post)
    db.session.commit()

    return {"Status": "Updated"}, 200


# @hello_urls.route("/api/v1/who-i-am/<int:user_id>", methods=['GET'])
# @login_required
# def api_for_who_i_am(user_id):
#     if user_id != g.user_id:
#         return {"Error": "Requested data is not yours"}

# Working code 
@hello_urls.route('/api/v1/<user_id>/posts', methods=['GET'])
@login_required
def get_user_post(user_id):
    """Список постів юзера"""
    user_post = []
    post = Post.query.filter(Post.author_id==user_id).all()
    for i in post:
        user_post.append({
            "author_id": i.author_id,
            "title": i.title,
            "body": i.body,
            "created": i.created
        })

    return {"user_list_post": user_post}, 200

# Working code
@hello_urls.route('/api/v1/<user_id>/post/<post_id>', methods=['GET'])
@login_required
def user_post(user_id, post_id):
    """Виводимо пост користувача"""
    post = Post.query.filter(Post.id == post_id, Post.author_id == user_id).one()
    
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created
    }, 200

# Working code
@hello_urls.route('/api/v1/edit-user-info/<user_id>', methods=['PUT'])
@login_required
def edit_user_info(user_id):
    data = request.json
    _phone_number = data['phone_number']
    _first_name = data['first_name']
    _second_name = data['second_name']

    user_info = User.query.filter(User.id==user_id).first()

    # if user_info is _phone_number:
    #     return (f'This {_phone_number} is already exists')
    
    new_info = User(phone_number=_phone_number, first_name=_first_name, second_name=_second_name)

    db.session.add(new_info)
    db.session.commit()
    
    return {"Status": "Info about user was changed"}, 200


@hello_urls.route('/api/vi/change-user-password/<user_id>', methods=['PUT'])
@login_required
def change_user_password(user_id):
    data = request.json
    old_password = data['old_password']
    new_password = data['new_password']         

    user = User.query.filter(User.id == user_id).first()

    # if new_password == old_password:
    # # if check_password_hash(password_hash, password)    
    #     return {'Password confirmed. You can change new password'}
    # user.password = generate_password_hash(new_password)
    new_password = User(generate_password_hash(new_password, method='sha256'))
    # db.session.add(new_password)
    db.session.commit()

    return {"Status": "Password changed"}, 200

# Working code
@hello_urls.route('/api/v1/create-comments/<user_id>', methods=['POST'])
def create_comment(user_id):
    """Додавання нового коментаря"""
    data = request.json
    author_id = None
    post_id = None
    text = data['text']
    created = data['created']
    is_deleted = None

    new_comm = Comments(text=text, created=datetime.datetime.now(), author_id=user_id, post_id=user_id)
    
    db.session.add(new_comm)
    db.session.commit()

    return {"Status": "Comment created"}, 200

# Working code
@hello_urls.route('/api/v1/<comment_id>/update-comments/<user_id>', methods=['PUT'])    
def update_comment(comment_id, user_id):
    """Редагування(оновлення) коментарів"""
    data = request.json
    text = data['text']
    created = data['created']

    comment = Comments.query.filter(Comments.id == comment_id, Comments.author_id == user_id).first()
    if not comment:
        return {"Error": "This user hasn't comments"}
    
    comment.text = text
    comment.created = datetime.datetime.now()

    db.session.commit()
    return {"Status": "Comment updated"}, 200

# Working code
@hello_urls.route('/api/v1/<user_id>/delete-comment', methods=['DELETE'])
@login_required
def delete_comment(user_id):
    """Видалення коментарів"""
    comment = Comments.query.get(user_id)
    db.session.delete(comment)
    db.session.commit()

    return {"Status": "Comment deleted"}


@hello_urls.route('/api/v1/upload-files', methods=['POST'])
# @login_required
def upload_files():
    file = request.json['file']
    if not file:
        return {"No file uploaded"}, 400
    upload = Upload(name=file.name, url=file.url)
    db.session.add(upload)
    db.session.commit()

    # uploaded_files = request.files['file']
    # if uploaded_files.filename != '':
    #     uploaded_files.save(secure_filename(uploaded_files.filename))

    return {"File downloaded"}, 200    



