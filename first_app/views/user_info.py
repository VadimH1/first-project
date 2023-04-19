from flask import Flask, render_template, request, Blueprint

info_user = Blueprint("info", __name__)
 
@info_user.route("/user-info", methods=['GET', 'POST'])
def user_info_form():
    return render_template("user-info.html") 