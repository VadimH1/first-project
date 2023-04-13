from flask import Flask, render_template, request, Blueprint

create_post = Blueprint("create post", __name__)

@create_post.route("/create-post", methods=['GET', 'POST'])
def create_post_form():
    return render_template("create-post.html")