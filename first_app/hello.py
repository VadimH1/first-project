
import os
import json
import jwt
from flask import Flask, request, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask import g, request, redirect, url_for

app = Flask(__name__, template_folder='templates')
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'hello.sqlite'),
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from . import db
db.init_app(app)


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

    db = get_db()
    db.execute(
        "INSERT INTO user (phone_number, first_name, second_name, password) VALUES (?, ?, ?, ?)",
        (phone_number, first_name, second_name, generate_password_hash(password)),
    )
    db.commit()
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
        if not token_user_id or user_id != token_user_id:
            return {"error": "Користувач не авторизований"}, 403
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?",
            (token_user_id,),
        ).fetchone()

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

    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE phone_number = ?",
        (income_phone_number,),
    ).fetchone()
    # Перевірка, чи користувач існує
    if not user:
        return {"error": f"Користувач не існує з телефоном {income_phone_number}"}, 404

    if not check_password_hash(user['password'], income_password): # "reretrerf328432y4324dejbcf" != "password1"
        return {"error": f"Паролі не співпадають {income_phone_number}"}, 404

    # user_id має знаходитись в середині JWT.
    token_data = {"user_id": user["id"]}
    access_token = jwt.encode(token_data, SECRET, algorithm='HS256')
    return {"access_token": access_token}, 200

# J

@app.route("/api/v1/user-info/<user_id>", methods=['GET'])
# @is_authenticated https://pythonworld.ru/osnovy/dekoratory.html
# Треба створити декоратор, який буде дозволяти доступ до апі тільки залогіненим користувачам.
@login_required
def user_info_api(user_id):
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE id = ?",
        (user_id,),
    ).fetchone()
    return {
        "id": user["id"],
        "phone_number": user["phone_number"],
        "first_name": user["first_name"],
        "second_name": user["second_name"],
    }, 200


@app.route("/api/v1/who-i-am/<user_id>", methods=['GET'])
@login_required
def api_for_who_i_am(user_id):
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE id = ?",
        (user_id,),
    ).fetchone()
    return {
        "i_am": f"{user['first_name']} {user['second_name']}"
    }, 200

@app.route("/hello")
# @is_authenticated
def hello():
    return "Hello Andy"
