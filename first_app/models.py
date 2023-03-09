from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from .db import db      #from first_app.db import Base
from datetime import datetime


class User(db.Model):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	phone_number = Column(Text(), unique=True)
	first_name = Column(Text(), unique=False)
	second_name = Column(Text(), unique=False)
	password = Column(Text(), unique=False)
	
	
	def __init__(
		self, phone_number=None, 
		first_name=None, second_name=None, 
		password=None
	):
		self.phone_number = phone_number
		self.first_name = first_name
		self.second_name = second_name
		self.password = password
		
		
	def __repr__(self):
		return f'<User {self.phone_number}>'


	def full_name(self):
		return f'{self.first_name} {self.second_name}'
		

class Post(db.Model):
	__tablename__ = 'post'
	id = Column(Integer, primary_key=True)
	author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
	title = Column(String(100), nullable=False)
	body = Column(String(100), nullable=False)
	is_deleted = Column(Boolean(), default=False)
	created =Column(DateTime, nullable=False, default=datetime.utcnow())
	

	def __init__(self, author_id=None, title=None, body=None, created =None):
		self.author_id = author_id
		self.title = title
		self.body = body
		self.created = created


	def __repr__(self):
		return f'Post("{self.title}", "{self.body}", "{self.created}")'

class Comments(db.Model):
	__tablename__ = 'comments'

	id = Column(Integer, primary_key=True)
	author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
	post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
	text = Column(String(100), nullable=False)
	is_deleted = Column(Boolean(), default=False)
	created =Column(DateTime, nullable=False, default=datetime.utcnow())
