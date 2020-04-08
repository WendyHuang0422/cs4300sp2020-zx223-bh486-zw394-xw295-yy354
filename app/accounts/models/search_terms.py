from . import *
import 
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

	def __init__(self, user_query, terms_query):
		self.user_ip = user_ip
		self.date_posted = date_posted
		self.user_query = user_query
		self.terms_query = terms_query
		self.combined_query = combined_query

	def __repr__(self):
		return '<id {}>'.format(self.id)

# class Search_terms_Schema(ModelSchema):
#   	class Meta:
#     	model = Search_terms

# class User_searches(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
