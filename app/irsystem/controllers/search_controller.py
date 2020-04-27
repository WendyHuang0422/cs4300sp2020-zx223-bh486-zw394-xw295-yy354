from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from flask import request, jsonify

from app import db
from app.accounts.models.search_terms import Search_terms, Search_users, Tweet_checks
from flask_sqlalchemy import SQLAlchemy

from random import randint

import tweepy, re, datetime, urllib, json, math, nltk, pymongo, datetime
nltk.download('stopwords')
import numpy as np

from pymongo import MongoClient
from datetime import timedelta
from newspaper import Article

import adhoc_data_crawl

import time


# how many tweets we are retrieving, and how many news for each tweet we are retrieving
length_retrieval_tweets = 20
length_retrieval_news = 20

@irsystem.route("/", methods=['GET', 'POST'])
def search():
	return render_template("search.html")

@irsystem.route("/results", methods=['GET', 'POST'])
def search_for():
	user = request.args.get('search')
	topic = request.args.get('terms')

	leaning = {"abc-news" : 1, "associated-press" : 2, "bloomberg" : 2, "cbs-news" : 1, "nbc-news" : 1, \
	'fox-news' : 3, 'reuters' : 2, 'usa-today' : 2, 'business-insider' : 2, 'the-hill' : 2, 'espn' : 1, \
	'axios' : 1, 'bbc' : 2}
	leaning_ref = ["left", "lean-left", "central", 'lean-right', 'right']
	color = {"left": "#e97676", "lean-left": "#e4a5a5", "central": "#d1d1d1", "lean-right": \
	"#a5c0e4", "right": "#7fa2d1"}

	if topic == "": topic = None

	length = 0
	data = []
	date = []
	retweets = []
	like = []
	news_list = []
	error = []
	# padding = "_".ljust(len(user) + 2, "_")
	start_time = time.time()

	try:
		# result = adhoc_data_crawl.totally_aggregated(user, 3, False, topic, N_keyword = 5, \
		# 	num_processed_tweets = 100, num_pool_tweets = 200, nltk1 = True)
		result = adhoc_data_crawl.totally_aggregated(user, 3, False, topic, N_keyword = 5, \
			num_processed_tweets = 20, num_pool_tweets = 40, nltk1 = True)
		length = min(len(result[0]), 3)

		for i in range(length):
			tweet = result[0][i][0]
			data.append(tweet["text"])
			date.append(tweet["created_at"])
			retweets.append(tweet["retweet_count"])
			like.append(tweet["favorite_count"])
			tweet_news = []

			for news in result[1][i]:
				source = news[0]["source"]
				if source in leaning.keys():
					source_leaning = leaning_ref[leaning[source]]
					source_color = color[source_leaning]
				else:
					source_color = "white"
				# title truncator
				title = news[0]["description"]
				if len(title) > 154:
					title = title[0 : 150] + " ..."
				tweet_news.append((source, title, news[0]["url"], \
					source_color, news[1]))
			news_list.append(tweet_news)
		
	except tweepy.TweepError as err:
		print("Oops, something went wrong!")
		if err.reason.find("status code = 404") > -1:
			print("Houston, we got a TweepError 404")
			error_msg = "User \"" + user + "\" either does not exist, or the user is inactive."
			error.append(error_msg)
			error.append("TweepyError code: 404")
		else:
			error.append("An error occured, please try another search.")

	time_taken = round(time.time() - start_time, 5)
	
	return render_template("results.html", \
		user = user, topic = topic, \
		data = data, length = length, date = date, retweets = retweets, like = like, \
		news_list = news_list, \
		error = error, time_taken = time_taken)













