from flask import Flask, render_template, request, Blueprint

update_post = Blueprint("upd_post", __name__)

@update_post.route("/update/post/<int:post_id>", methods=['GET', 'POST'])
def update_user_post(post_id):
    return render_template("update-post.html")