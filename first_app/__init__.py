import os
from flask import Flask

from .hello import hello_urls

from flask_alembic import Alembic
# from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):
    app = Flask(__name__, template_folder='templates', instance_relative_config=True)
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/hello.sqlite"
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'hello.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    app.register_blueprint(hello_urls)

    # db = SQLAlchemy(app)

    alembic = Alembic()
    alembic.init_app(app)

    # with app.app_context():
    #     alembic.revision('making changes')
    #     alembic.upgrade()
    #     environment_context = alembic.env

    return app

if __name__ == '__main__':
    create_app().run(debug=True)