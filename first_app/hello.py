
import os
import json
import jwt
from flask import Flask, Blueprint, request, render_template, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> c3ce9c5 (check)
from flask import g, request, redirect, url_for
from .models import Post, User
from .db import get_db, db_session
from . import db
<<<<<<< HEAD
=======
from flask import g, request, redirect, url_for, Blueprint
from models import Post, User
from db import get_db, db_session
from . import db, app
=======
>>>>>>> c3ce9c5 (check)

>>>>>>> 20d724a (After fixed conflicts)

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
<<<<<<< HEAD
@hello_urls.route("/api/v1/register-user", methods=['POST'])
=======
# <<<<<<< HEAD
# @app.route("/api/v1/register-user", methods=['GET','POST'])
# =======
@hello_urls.route("/api/v1/register-user", methods=['POST'])
# >>>>>>> 5801257e45f5140cf60060d209571b20f6a09351
>>>>>>> 20d724a (After fixed conflicts)
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
# @is_authenticated https://pythonworld.ru/osnovy/dekoratory.html
# Треба створити декоратор, який буде дозволяти доступ до апі тільки залогіненим користувачам.
@login_required
def user_info_api(user_id):
    user = User.query.filter(User.id == user_id).one()
    return {
        "id": user["id"],
        "phone_number": user["phone_number"],
        "first_name": user["first_name"],
        "second_name": user["second_name"],
    }, 200
    
    
@hello_urls.route('/api/v1/user-posts/<user_id>', methods=['POST'])
@login_required
def create_post(user_id):
    posts = Post.query.all()
    posts = []
    for post in posts:
        posts.append({
        "id": post["id"],
        "title": post["title"],
        "body": post["body"],
        "created": post["created"],	
	})    
    return json(posts)
    

@hello_urls.route('/api/v1/edit-posts/<user_id>', methods=['GET','POST'])
def post_edit(user_id):
    data = request.json
    post = Post.query.get(user_id)
    if request.method == "POST":
        post.title = data['title']
        post.body = data['body']
        post.created = data['created']
        db.session.commit()
            		        
    return "Post edited", 200	
    
    
@hello_urls.route('/api/v1/delete-post/<user_id>', methods=['GET','POST'])
def delete_posts(post_id):
    post = Post.query.filter_by(id=post_id, user_id=User.id).first()
    db.session.delete(post)
    db.session.commit()
        
    return "Post deleted", 200
    

@hello_urls.route("/api/v1/who-i-am/<int:user_id>", methods=['GET'])
@login_required
def api_for_who_i_am(user_id):
    if user_id != g.user_id:
        return {"error": "Requested data is not yours"}

 
@hello_urls.route('/api/v1/<user_id>/posts/<post_id>', methods=['GET'])
def get_user_posts(post_id):
    """Виведення постів по користувачу. Виводимо пост користувача"""
    post = Post.query.get(post_id)
    return "Отримали пост користувача", 200

# https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query -> вивчити
    user = User.query.filter(User.id == user_id).one()

