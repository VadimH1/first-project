import sqlite3
import click

from flask import current_app, g

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(f'sqlite:///instance/hello.sqlite')
db_session = scoped_session(sessionmaker(autocommit=False, 
                                         autoflush=False, 
                                         bing=engine))

Base = declarative_base()
Base.query = db_session.query_property()

db = SQLAlchemy()

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# def get_db():
#     """
#         Створюємо з'єднання з базою данних
#     """
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row

#     return g.db

# def init_db():
#     """
#        Створює таблиці в базі данних
#     """
#     import models
#     Base.metadata.create_all(bind=engine)
    

# @click.command('init-db')
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')


# def init_app(app):
#     from flask_alembic import alembic_click
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)
#     app.cli.add_command(alembic_click, "db")
