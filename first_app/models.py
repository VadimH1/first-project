from sqalchemy import Column, Integer, String, Text, DateTime, ForeignKeyConstraint
from first_app.db import Base


class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	phone_number = Column(Text(), unique=True)
	first_name = Column(Text(), unique=False)
	second_name = Column(Text(), unique=False)
	password = Column(Text(), unique=False)
	
	def __init__(
		self, phone_number=None, 
		first_name=None, second_name=None, 
		passwor=None
	):
		self.phone_number = phone_number
		self.first_name = first_name
		self.second_name = second_name
		self.password = password
		
		
	def __repr__(self):
		return f'<User {self.phone_number}>'
		
	def full_name(self):
		return f'{self.first_name} {self.second_name}'
		

class Post(Base):
	__tablename__ = 'post'
	id = Column(Integer, primary_key=True)
	#author_id = Column(Integer, nullable=False)
	title = Column(String(100), nullable=False)
	body = Column(String(100), nullable=False)
	created =Column(TimeStamp(), .....)
	
	__table_args__ = (
		ForeignKeyConstraint(["author_id"], ["user.id"])
	)	
	
	def __init__(self, title=None, body=None, created =None):
		self.title = title
		self.body = body
		self.created = created
		
	def __repr__(self):
		return f'Post("{self.title}", "{self.body}", "{self.created}")'			
		
		
		
