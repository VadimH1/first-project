from flask import Flask, render_template, request, Blueprint

login = Blueprint("login", __name__)
 
@login.route("/login", methods=['GET', 'POST'])
def login_form():
    return render_template("login.html")   