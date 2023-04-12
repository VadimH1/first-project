import os
from flask import Flask

from .hello import hello_urls, post_urls, comment_urls, upload_urls

from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(test_config=None):
    app = Flask(__name__, template_folder='templates', instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
    app.config.from_mapping(
        SECRET_KEY = 'dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import db
    db.init_app(app)
    migrate = Migrate(app, db)
    
    ma = Marshmallow(app)

    app.register_blueprint(hello_urls)
    app.register_blueprint(post_urls)
    app.register_blueprint(comment_urls)
    app.register_blueprint(upload_urls)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)