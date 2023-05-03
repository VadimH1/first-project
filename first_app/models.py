from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from db import db
from datetime import datetime
from sqlalchemy.orm import relationship


class User(db.Model):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	phone_number = Column(String(), unique=True)
	first_name = Column(String(), unique=False)
	second_name = Column(String(), unique=False)
	password = Column(String(), unique=False)
	
	
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


class Upload(db.Model):
	__tablename__ = 'upload'
	id = Column(Integer, primary_key=True)
	url = Column(String(200))
	author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
	post = relationship("Post", back_populates="file", single_parent=True)

	def __init__(self, author_id=None, url=url):
		self.author_id = author_id
		self.url = url
		


class Post(db.Model):
	__tablename__ = 'post'
	id = Column(Integer, primary_key=True)
	author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
	title = Column(String(100), nullable=False)
	body = Column(String(100), nullable=False)
	is_deleted = Column(Boolean(), default=False)
	created = Column(DateTime, nullable=False, default=datetime.utcnow())
	image_id = Column(Integer, ForeignKey('upload.id'))

	comments = relationship("Comments", backref = "post")
	file = relationship("Upload", back_populates="post", primaryjoin=Upload.id==image_id)

	def __init__(self, author_id=None, title=None, body=None, is_deleted=None, created=None, image_id=None):
		self.author_id = author_id
		self.title = title
		self.body = body
		self.is_deleted = is_deleted
		self.image_id = image_id
		self.created = datetime.utcnow()


	def __repr__(self):
		return f'Post("{self.title}", "{self.body}", {self.created})'


class Comments(db.Model):
	__tablename__ = 'comments'
	id = Column(Integer, primary_key=True)
	author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
	post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
	text = Column(String(100), nullable=False)
	created = Column(DateTime, nullable=False, default=datetime.utcnow())
	is_deleted = Column(Boolean(), default=False)

	def __init__(self, author_id=None, post_id=None, text=None, created=None, is_deleted=None):
		self.author_id = author_id
		self.post_id = post_id
		self.text = text
		self.is_deleted = is_deleted
		self.created = datetime.utcnow()


	def __repr__(self):
		return f'Comments({self.author_id}, {self.text}, {self.created})'	



	
