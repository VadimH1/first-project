import sqlite3
import click

from flask import current_app, g, session

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
