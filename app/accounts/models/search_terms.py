from . import *
from app import db 
from sqlalchemy.dialects.postgresql import JSON

class Search_terms(db.Model):
	__tablename__ = 'search_terms'

	id = db.Column(db.Integer, primary_key=True)
	user_query = db.Column(db.String())
	terms_query = db.Column(db.String())

	def __init__(self, user_query, terms_query):
		self.user_query = user_query
		self.terms_query = terms_query

	def __repr__(self):
		return '<id {}>'.format(self.id)

# class Search_terms_Schema(ModelSchema):
#   	class Meta:
#     	model = Search_terms
