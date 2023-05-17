from flask import Flask, render_template, request, Blueprint

edit_user_info = Blueprint("upd_info", __name__)

@edit_user_info.route("/edit-user-info", methods=['GET', 'POST'])
def update_user_info():
    return render_template("edit-user-info.html")