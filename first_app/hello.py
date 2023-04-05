
import os
import json 
import jwt
from flask import Flask, Blueprint, request, render_template, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask import g, redirect, url_for
from .models import Post, User, Comments, Upload
from .schemas import PostSchema, UserSchema, CommentsSchema, UploadSchema
from .db import db
from werkzeug.utils import secure_filename
from .config import SECRET_KEY, UPLOAD_FOLDER
import datetime


hello_urls = Blueprint("sync", __name__)
post_urls = Blueprint("post", __name__)
comment_urls = Blueprint("comment", __name__)
upload_urls = Blueprint("upload", __name__)


@hello_urls.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        print("Ми викликали GET")
        return render_template("index.html")

    if request.method == "POST":
        print("Ми викликали POST")
        form = request.form 

        _data = {
            "fname": form["fname"],
            "lname": form["lname"]
        }
        return render_template("index.html", income_form_data=_data)
    
@hello_urls.route("/register", methods=['GET', 'POST'])
def registation_form():
        return render_template("registration.html")
    
@hello_urls.route("/login", methods=['GET', 'POST'])
def login_form():
    return render_template("login.html")    

@hello_urls.route("/create-post", methods=['GET', 'POST'])
def create_post_form():
    return render_template("create-post.html")
        

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

    user_schema = UserSchema()

    return jsonify(user_schema.dump(user))
    # return {"Status": "User was reistrate"}


def login_required(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
         
        access_token = request.headers.get("Authorization")
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"]) # .decode("utf-8")
        token_user_id = payload["user_id"] 
        g.user_id = token_user_id 
        
        if not access_token:
            return {"Error": "access_token"}, 400
    
        if not token_user_id:
            return {"error": "Користувач не авторизований"}, 403
            
        user = User.query.filter(User.id == token_user_id).first()

        if not user:
            return {"error": f"Користувач не існує"}, 404
        
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


@hello_urls.route("/api/v1/user-info/<user_id>", methods=['GET'])
@login_required
def user_info_api(user_id):
    user = User.query.filter(User.id == user_id).first()
    
    if not user:
        return {"Неверный логин или пароль"}, 400
    
    user_schema = UserSchema(many=True)
    
    return jsonify(user_schema.dump(user)) # {"info": user.full_name()}, 200
    
   
@post_urls.route('/api/v1/create-post', methods=['POST'])
@login_required
def create_post():
    """Створення постів"""
    author_id = g.user_id   
    data = request.json
    title = data['title']
    body = data['body']
    created = data['created']

    post = Post(author_id=author_id,title=title, body=body, created=datetime.datetime.utcnow())
    db.session.add(post)
    db.session.commit()

    post_schema = PostSchema()
    
    return jsonify(post_schema.dump(post)) 
    
    
@post_urls.route('/api/v1/delete-post/<user_id>', methods=['DELETE'])
@login_required
def delete_post(user_id):
    """Видалення постів"""
    post = Post.query.get(user_id)
    db.session.delete(post)
    db.session.commit()
        
    return {"Status": "Deleted post"}, 200


@post_urls.route('/api/v1/update-post/<post_id>/<user_id>', methods=['PUT'])
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
    post.created = datetime.datetime.utcnow()

    db.session.add(post)
    db.session.commit()

    post_schema = PostSchema(many=True)

    return jsonify(post_schema.dump(post)) 

 
@post_urls.route('/api/v1/<user_id>/posts', methods=['GET'])
@login_required
def get_user_post(user_id):
    """Список постів юзера"""
    user_post = []
    post = Post.query.filter(Post.author_id==user_id).all()
    # for i in post:
    #     user_post.append({
    #         "author_id": i.author_id,
    #         "title": i.title,
    #         "body": i.body,
    #         "created": i.created
    #     })
    post_schema = PostSchema(many=True)

    return jsonify(post_schema.dump(post))


@post_urls.route('/api/v1/<user_id>/post/<post_id>', methods=['GET'])
@login_required
def user_post(user_id, post_id):
    """Виводимо пост користувача"""
    post = Post.query.filter(Post.id == post_id, Post.author_id == user_id).first()
    
    user_post_schema = PostSchema(many=True)

    return jsonify(user_post_schema.dump(post))


@hello_urls.route('/api/v1/edit-user-info/<user_id>', methods=['PUT'])
@login_required
def edit_user_info(user_id):
    data = request.json
    _phone_number = data['phone_number']
    _first_name = data['first_name']
    _second_name = data['second_name']
    _password = data['password']

    user_info = User.query.filter(User.id==user_id).first()
    
    new_info = User(phone_number=_phone_number, first_name=_first_name, second_name=_second_name, password=_password)

    db.session.add(new_info)
    db.session.commit()

    user_schema = UserSchema(many=True)
    
    return jsonify(user_schema.dump(new_info))


@hello_urls.route('/api/vi/change-user-password/<user_id>', methods=['PUT'])
@login_required
def change_user_password(user_id):
    data = request.json
    old_password = data['old_password']
    new_password = data['new_password']         

    user = User.query.filter(User.id == user_id).first()

    user.password = generate_password_hash(new_password, method='sha256')

    db.session.commit()

    user_schema = UserSchema(many=True)

    return jsonify(user_schema.dump(user))


@comment_urls.route('/api/v1/create-comments/<user_id>', methods=['POST'])
@login_required
def create_comment(user_id):
    """Додавання нового коментаря"""
    data = request.json
    author_id = None
    post_id = None
    text = data['text']
    created = data['created']
    is_deleted = None

    new_comm = Comments(
        text=text,
        created=datetime.datetime.utcnow(),
        author_id=user_id, post_id=user_id
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


@upload_urls.route('/api/v1/upload-files', methods=['POST'])
def upload_files():
    uploaded_files = request.files['file']

    if uploaded_files.filename != '':
        uploaded_files.save(secure_filename(uploaded_files.filename))

    path_to_file = uploaded_files.save(os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_files.filename)))    
    upload = Upload(url = uploaded_files.filename)
    db.session.add(upload)
    db.session.commit()

    upload_schema = UploadSchema()
    return jsonify(upload_schema.dump(upload))    



