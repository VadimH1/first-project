from flask import render_template, request, Blueprint

index_urls = Blueprint("index", __name__)

@index_urls.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")