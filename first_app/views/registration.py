from flask import render_template, request, Blueprint

register_urls = Blueprint("register", __name__)

@register_urls.route("/register", methods=['GET', 'POST'])
def registation_form():
    return render_template("registration.html")