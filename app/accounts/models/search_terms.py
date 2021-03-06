from . import *
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db 
from sqlalchemy.dialects.postgresql import JSON

class Search_terms(db.Model):
	__tablename__ = 'search_terms'

	id = db.Column(db.Integer, primary_key=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_ip = db.Column(db.String())
	user_query = db.Column(db.String())
	terms_query = db.Column(db.String())
	combined_query = db.Column(db.String())

	def __init__(self, user_ip, user_query, terms_query, combined_query):
		self.user_ip = user_ip
		self.user_query = user_query
		self.terms_query = terms_query
		self.combined_query = combined_query

	def __repr__(self):
		return '<id {}>'.format(self.id)

class Search_users(db.Model):
	__tablename__ = 'search_users'

	id = db.Column(db.Integer, primary_key=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_ip = db.Column(db.String())
	user_query = db.Column(db.String())

	def __init__(self, user_ip, user_query):
		self.user_ip = user_ip
		self.user_query = user_query

	def __repr__(self):
		return '<id {}>'.format(self.id)

class Tweet_checks(db.Model):
	__tablename__ = 'tweet_checks'

	id = db.Column(db.Integer, primary_key=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	tweet_author = db.Column(db.String())
	tweet_str = db.Column(db.String())
	tweet_time = db.Column(db.String())
	combined_str = db.Column(db.String())
	user_ip = db.Column(db.String())

	def __init__(self, user_ip, user_query):
		self.user_ip = user_ip
		self.tweet_author = tweet_author
		self.tweet_str = tweet_str
		self.tweet_time = tweet_time

	def __repr__(self):
		return '<id {}>'.format(self.id)

# class Search_topic(db.Model)
# 	__tablename__ = 'search_topic'

# 	id = db.Column(db.Integer, primary_key=True)
# 	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
# 	user_ip = db.Column(db.String())
# 	user_query = db.Column(db.String())
# 	terms_query = db.Column(db.String())
# 	combined_query = db.Column(db.String())

# 	def __init__(self, user_ip, user_query, terms_query, combined_query):
# 		self.user_ip = user_ip
# 		self.user_query = user_query
# 		self.terms_query = terms_query
# 		self.combined_query = combined_query

# 	def __repr__(self):
# 		return '<id {}>'.format(self.id)

# class Search_terms_Schema(ModelSchema):
#   	class Meta:
#     	model = Search_terms

# class User_searches(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
