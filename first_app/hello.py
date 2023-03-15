
import os
import json #jsonify ?
import jwt
from flask import Flask, Blueprint, request, render_template, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask import g, redirect, url_for
from .models import Post, User, Comments
from . import db
from werkzeug.utils import secure_filename

# app = create_app()

hello_urls = Blueprint("sync", __name__)

@hello_urls.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        print("Ми викликали GET")
        return render_template("index.html")

    if request.method == "POST":
        print("Ми викликали POST")
        form = request.form # ImmutableMultiDict([('fname', 'Andy'), ('lname', 'KOOccccc')])
        # import pdb; pdb.set_trace()
        _data = {
            "fname": form["fname"],
            "lname": form["lname"]
        }
        return render_template("index.html", income_form_data=_data)

# Add comment to the api
@hello_urls.route("/api/v1/register-user", methods=['POST'])
def register_user_api():
    data = request.json
    phone_number = data["phone_number"]
    first_name = data["first_name"]
    second_name = data["second_name"]
    password = data["password"]
    
    user = User('phone_number', 'first_name', 'second_name', 'password')
    db.session.add(user)
    db.session.commit()

    return {}, 200


def login_required(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):

        user_id = int(kwargs.get("user_id"))
            # JSON WEB TOKEN 
        access_token = request.headers.get("Authorization")
        payload = jwt.decode(access_token, app.config['SECRET_KEY'], algorithms=["HS256"])
        token_user_id = payload["user_id"]
            # 1) Взяти токен з headers Authorization.
            # 2) Валідувати токен за допомогою бібліотек.
            # 3) Дістати user_id з payload і зробити перевірки.
        if not token_user_id:
            return {"error": "Користувач не авторизований"}, 403
        
        user = User.qurey.filter(User.id == token_user_id).one()

        if not user:
            return {"error": f"Користувач не існує  {user_id}"}, 404

        if int(token_user_id) != user["id"]:
            return {"error": "Користувач запитує не свою інформацію"}, 403

        return f(*args, **kwargs)
    return _wrapper

@hello_urls.route("/api/v1/login", methods=['POST'])
def login_api():
    data = request.json # Analog

    income_phone_number = data.get("phone_number") # Данні з запиту
    income_password = data.get("password") # Данні з запиту
    # "dsfdfdsfsfd" -> sha1(income_password)

    if not income_phone_number or not income_password:
        return "", 401
        
    user = User.query.filter(User.id == income_phone_number).one()
    
    if not user:
        return {"error": f"Користувач не існує з телефоном {income_phone_number}"}, 404

    if not check_password_hash(user['password'], income_password): # "reretrerf328432y4324dejbcf" != "password1"
        return {"error": f"Паролі не співпадають {income_phone_number}"}, 404

    # user_id має знаходитись в середині JWT.
    token_data = {"user_id": user["id"]}
    access_token = jwt.encode(token_data, app.config['SECRET_KEY'], algorithm='HS256') 
    return {"access_token": access_token}, 200


@hello_urls.route("/api/v1/user-info/<user_id>", methods=['GET'])
@login_required
def user_info_api(user_id):
    user = User.query.filter(User.id == user_id).one()
    return {
        "id": user["id"],
        "phone_number": user["phone_number"],
        "first_name": user["first_name"],
        "second_name": user["second_name"],
    }, 200
    
    
@hello_urls.route('/api/v1/create-post/<user_id>', methods=['POST'])
@login_required
def create_post(user_id):
    """Створення постів"""
    data = request.json
    title = data['title']
    body = data['body']
    created = data['create']	
    author_id = None

    post = Post(title, body, created, author_id)
    db.session.add(post)
    db.session.commit()

    return "Create", 200
    
    
@hello_urls.route('/api/v1/delete-post/<user_id>', methods=['DELETE'])
@login_required
def delete_post(user_id):
    """Видалення постів"""
    post = Post.query.get(user_id)
    db.session.delete(post)
    db.session.commit()
        
    return "Deleted", 200


@hello_urls.route('/api/v1/update-post/<user_id>', methods=['PUT'])
@login_required
def update_post(user_id):
    """Редагування постів"""
    data = request.json
    title = data['title']
    body = data['body']
    created = data['create']	
    author_id = None

    post = Post.query.get(user_id)
    db.session.commit()

    return "Updated", 200


@hello_urls.route("/api/v1/who-i-am/<int:user_id>", methods=['GET'])
@login_required
def api_for_who_i_am(user_id):
    if user_id != g.user_id:
        return {"error": "Requested data is not yours"}

 
@hello_urls.route('/api/v1/<user_id>/posts/', methods=['GET'])
@login_required
def get_user_post(user_id):
    """Список постів юзера"""
    post = Post.query.all(user_id)
    return "Отримали пости юзера", 200


@hello_urls.route('/api/v1/<user_id>/post/<post_id>', methods=['GET'])
@login_required
def user_post(post_id):
    """Виводимо пост користувача"""
    post = Post.query.get(post_id)
    return "Пост користувача", 200


@hello_urls.route('/api/v1/user-info/edit/<user_id>', methods=['PUT'])
@login_required
def edit_user_info(user_id):
    data = request.json
    _phone_number = data['phone_number']
    _first_name = data['first_name']
    _second_name = data['second_name']

    user_info = User.query.filter(User.phone_number==_phone_number).one()

    if user_info is _phone_number:
        return (f'This {_phone_number} is already exists')
    
    new_info = User(phone_number=_phone_number, first_name=_first_name, second_name=_second_name)
    db.session.add(new_info)
    db.commit()

    return {}, 200


@hello_urls.route('/api/vi/user-info/change-password', methods=['PUT'])
@login_required
def change_user_password(user_id):
    data = request.json
    old_password = data['password']
    new_password = data['new_password']

    user = User.query.filter(User.id==user_id)

    if old_password == user.password:
    # if check_password_hash(password_hash, password)    
        return {'Password confirmed. You can change new password'}
    
    new_password = User(new_password=generate_password_hash(new_password, method='sha256'))
    db.session.add(new_password)
    db.commit()

    return "Password changed", 200


@hello_urls.route('/api/v1/create-comments/<user_id>', methods=['POST'])
def create_comment(user_id):
    """Додавання нового коментаря"""
    data = request.json
    text = data['text']
    created = data['created']
    new_comm = Comments(text, created)
    
    db.session.add(new_comm)
    db.commit()

    comment = Comments.query.get(new_comm.id)
    return "Comment created", 200


@hello_urls.route('/api/v1/update-comments/<user_id>', methods=['PUT'])    
def update_comment(user_id):
    """Редагування(оновлення) коментарів"""
    data = request.json
    comment = Comments.query.get(user_id)
    text = data['text']
    created = data['created']

    comment.text = text
    comment.created = created

    db.session.commit()
    return "Comment updated", 200


@hello_urls.route('/api/v1/delete-comments', methods=['DELETE'])
def delete_comment(user_id):
    """Видалення коментарів"""
    comment = Comments.query.get(user_id)
    db.session.delete(comment)
    db.commit()

    return "Comment deleted", 200


@hello_urls.route('/api/v1/upload-files', methods=['POST'])
def upload_files():
    uploaded_files = request.files['file']
    if uploaded_files.filename != '':
        uploaded_files.save(secure_filename(uploaded_files.filename))

    return "Added images"    


