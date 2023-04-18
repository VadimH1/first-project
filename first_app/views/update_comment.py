from flask import Flask, render_template, request, Blueprint

update_comment = Blueprint("update_comment", __name__)

@update_comment.route("/update/comment/<int:comment_id>", methods=['GET', 'POST'])
def update_user_comment(comment_id):
    return render_template("update-comment.html")