import os
import json 
import jwt
from flask import Flask, Blueprint, request, session, jsonify, g
from werkzeug.security import generate_password_hash
from functools import wraps
from models import User
from schemas import UserSchema
from db import db
from config import SECRET_KEY

hello_urls = Blueprint("user", __name__)


def login_required(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
         
        access_token = request.headers.get("Authorization")
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
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


@hello_urls.route("/api/v1/user-info", methods=['GET'])
@login_required
def user_info_api():
    # author_id = g.user_id

    user = User.query.filter(User.id == g.user_id).first()
    
    if not user:
        return {"Неверный логин или пароль"}, 400
    
    user_schema = UserSchema()
    
    return jsonify(user_schema.dump(user))


@hello_urls.route('/api/v1/edit-user-info', methods=['PUT'])
@login_required
def edit_user_info():
    data = request.json
    _phone_number = data['phone_number']
    _first_name = data['first_name']
    _second_name = data['second_name']
    # _password = data['password']

    user_info = User.query.filter(User.id==g.user_id).first()
    
    # new_info = User(phone_number=_phone_number, first_name=_first_name, second_name=_second_name) #password=_password)
    user_info.phone_number=_phone_number
    user_info.first_name=_first_name
    user_info.second_name=_second_name
    # db.session.add(new_info)
    db.session.commit()

    user_schema = UserSchema()
    
    return jsonify(user_schema.dump(user_info))


@hello_urls.route('/api/vi/change-user-password/<user_id>', methods=['PUT'])
@login_required
def change_user_password(user_id):
    data = request.json
    old_password = data['old_password']
    new_password = data['new_password']         

    user = User.query.filter(User.id == user_id).first()

    user.password = generate_password_hash(new_password, method='sha256')

    db.session.commit()

    user_schema = UserSchema()

    return jsonify(user_schema.dump(user))