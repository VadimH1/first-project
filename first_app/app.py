import os
from flask import Flask
# from .api_app import hello_urls, post_urls, comment_urls, upload_urls
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from views.index import index_urls
from views.create_post import create_post
from views.login_view import login
from views.registration import register_urls
from views.post import post
from views.update_post import update_post
from views.update_comment import update_comment
from views.user_info import info_user
from api_app.user_api import hello_urls
from api_app.upload_api import upload_urls
from api_app.post_api import post_urls
from api_app.comment_api import comment_urls

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir,'static/UploadFile')


def create_app(test_config=None):
    app = Flask(__name__, template_folder='templates', static_folder='static', instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
    app.config.from_mapping(
        SECRET_KEY = 'dev'
    )
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from db import db
    db.init_app(app)
    migrate = Migrate(app, db)
    
    ma = Marshmallow(app)

    app.register_blueprint(hello_urls)
    app.register_blueprint(post_urls)
    app.register_blueprint(comment_urls)
    app.register_blueprint(upload_urls)
    app.register_blueprint(index_urls)
    app.register_blueprint(register_urls)
    app.register_blueprint(post)
    app.register_blueprint(login)
    app.register_blueprint(create_post)
    app.register_blueprint(update_post)
    app.register_blueprint(update_comment)
    app.register_blueprint(info_user)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)