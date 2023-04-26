from flask import Flask, render_template, request, Blueprint

change_password = Blueprint("password_change", __name__)

@change_password.route("/change-password", methods=['GET', 'POST'])
def edit_user_password():
    return render_template("change-password.html")