from flask import Flask, render_template, request, Blueprint

post = Blueprint("posts", __name__)

@post.route("/post/<int:post_id>", methods=['GET', 'POST'])
def user_post(post_id):
    return render_template("post.html")