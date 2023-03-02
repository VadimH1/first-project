
import os
import json
import jwt
from flask import Flask, request, render_template, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask import g, request, redirect, url_for
from models import Post, User
from . import app
from . import db


SECRET = "frefrfrefrenfnrenfffdnvfvibrerberfn"
from .db import get_db

@app.route("/", methods=['GET', 'POST'])
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
@app.route("/api/v1/register-user", methods=['POST'])
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
        payload = jwt.decode(access_token, SECRET, algorithms=["HS256"])
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

@app.route("/api/v1/login", methods=['POST'])
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
    access_token = jwt.encode(token_data, SECRET, algorithm='HS256')
    return {"access_token": access_token}, 200


@app.route("/api/v1/user-info/<user_id>", methods=['GET'])
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
    
    
@app.route('/api/v1/user-posts/<user_id>', methods=['POST'])
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
    

@app.route('/api/v1/edit-posts/<user_id>', methods=['GET'])
def post_edit(user_id):
    data = request.json
    post = Post.query.get(user_id)
    if request.method == "POST":
        post.title = data['title']
        post.body = data['body']
        post.created = data['created']
        db.session.commit()
      #return redirect('/user-posts')
            		        
    return "Post edited", 200	
    
    
@app.route('/api/v1/delete-posts/<user_id>', methods=['POST'])
def delete_posts(post_id):
    post = Post.query.filter_by(id=post_id, user_id=User.id).first()
    db.session.delete(post)
    db.session.commit()
        
    return "Post deleted", 200
    

@app.route("/api/v1/who-i-am/<int:user_id>", methods=['GET'])
@login_required
def api_for_who_i_am(user_id):
    if user_id != g.user_id:
        return {"error": "Requested data is not yours"}

 
@app.route('/api/v1/<user_id>/posts/<post_id>', methods=['GET'])
def get_user_posts(post_id):
    """Виведення постів по користувачу. Виводимо пост користувача"""
    post = Post.query.get(post_id)
    return "Отримали пост користувача", 200

# https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query -> вивчити
    user = User.query.filter(User.id == user_id).one()

