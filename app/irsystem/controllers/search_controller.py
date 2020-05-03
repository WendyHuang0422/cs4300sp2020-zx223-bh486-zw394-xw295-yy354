import re
import time
import adhoc_data_crawl
from newspaper import Article
from datetime import timedelta
from pymongo import MongoClient
import numpy as np
from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from flask import request, jsonify

from app import db
from app.accounts.models.search_terms import Search_terms, Search_users, Tweet_checks
from flask_sqlalchemy import SQLAlchemy

from random import randint

import tweepy
import re
import datetime
import urllib
import json
import math
import nltk
import pymongo
import datetime
nltk.download('stopwords')


# how many tweets we are retrieving, and how many news for each tweet we are retrieving
length_retrieval_tweets = 20
length_retrieval_news = 20

num_tweets_to_show = 10

html_tag = re.compile(r'<[^>]+>')


def helper_remove_html_tags(raw_string):
    return html_tag.sub('', raw_string)


def helper_string_trunc(long_str, trunc_len):
    if len(long_str) < trunc_len:
        return helper_remove_html_tags(long_str)
    else:
        short_str = long_str[: trunc_len]
        last_space_idx = short_str.rfind(" ")
        if last_space_idx != -1:
            short_str = long_str[: last_space_idx]
        return helper_remove_html_tags(short_str) + " ... "


@irsystem.route("/", methods=['GET', 'POST'])
def search():
    return render_template("search.html")


@irsystem.route("/results", methods=['GET', 'POST'])
def search_for():
    user = request.args.get('search')
    topic = request.args.get('terms')

    leaning = {"ABC News": 1, "Associated Press": 2, "Bloomberg": 2, "CBS News": 1, "NBC News": 1,
               'Fox News': 3, 'Reuters': 2, 'USA Today': 2, 'Business Insider': 2, 'The Hill': 2, 'ESPN': 1,
               'Axios': 1, 'BBC News': 2}
    # leaning_ref = ["left", "lean-left", "central", 'lean-right', 'right']
    leaning_ref = ["Left", "Lean Left", "None", 'Lean Right', 'Right']

    fact = {"ABC News": 1, "Associated Press": 0, "Bloomberg": 2, "CBS News": 1, "NBC News": 1,
            'Fox News': 3, 'Reuters': 0, 'USA Today': 1, 'Business Insider': 1, 'The Hill': 2, 'ESPN': 1,
            'Axios': 1, 'BBC News': 1}
    # fact_ref = ["Very High", "High", "Mostly Factual", "Mixed", "Low", "Very Low"]
    fact_ref = ["Very High", "High", "Medium", "Mixed", "Low", "Very Low"]

    if topic == "":
        topic = None

    length = 0
    # contains user data: [display name, url, verified]
    tw_user_data = []
    # contains user x_counts: [followers, friends, listed, favourites, statuses]
    tw_user_counts = []
    # contains links for user media objects: [profile_banner_url, profile_image_url_https]
    tw_user_media_obj = []
    tw_id_str = []
    tw_text = []
    tw_text_trunc = []
    tw_date = []
    tw_retweets = []
    tw_like = []
    tw_sentiment = []
    news_list = []
    tw_news_num = []
    error = []
    # padding = "_".ljust(len(user) + 2, "_")
    start_time = time.time()
    xzh_wanted_user_keys = ["followers_count", "friends_count", "listed_count",
                            "favourites_count", "statuses_count", "profile_banner_url", "profile_image_url_https"]
    try:
        # result = adhoc_data_crawl.totally_aggregated(user, 3, False, topic, N_keyword = 5, \
        # 	num_processed_tweets = 100, num_pool_tweets = 200, nltk1 = True)
        result = adhoc_data_crawl.totally_aggregated(user, num_tweets_to_show, False, topic, N_keyword=5,
                                                     num_processed_tweets=20, num_pool_tweets=40, nltk1=True)

        length = min(len(result[0]), num_tweets_to_show)

        for i in range(length):
            tweet = result[0][i][0]
            # print(tweet)
            if i == 0:
                user_tw_acc_url = "https://twitter.com/" + user
                tweet_author = tweet["user"]
                tw_user_data = [tweet_author["name"],
                                user_tw_acc_url, tweet_author["verified"]]
                tw_user_counts = [tweet_author["followers_count"], tweet_author["friends_count"],
                                  tweet_author["listed_count"], tweet_author["favourites_count"],
                                  tweet_author["statuses_count"]]

                tw_user_media_obj = [tweet_author["profile_banner_url"],
                                     tweet_author["profile_image_url_https"]]

            tw_id_str.append(tweet["id_str"])
            tw_text.append(tweet["text"])
            tw_text_trunc.append(helper_string_trunc(tweet["text"], 170))
            time_stamp = tweet["created_at"].split(" ")
            time_o_clock = time_stamp[3].split(":")
            am_pm_time = ""
            if int(time_o_clock[0]) == 0:
                am_pm_time = am_pm_time + "12" + ":" + time_o_clock[1] + " AM"
            elif int(time_o_clock[0]) < 12:
                am_pm_time = am_pm_time + \
                    time_o_clock[0] + ":" + time_o_clock[1] + " AM"
            else:
                hour = int(time_o_clock[0]) - 12
                am_pm_time = am_pm_time + \
                    str(hour) + ":" + time_o_clock[1] + " PM"

            time_stamp_string = time_stamp[1] + \
                " " + time_stamp[2] + " " + am_pm_time
            tw_date.append(time_stamp_string)
            tw_retweets.append(tweet["retweet_count"])
            tw_like.append(tweet["favorite_count"])
            tw_sentiment.append(tweet["sentiment"])
            tweet_news = []
            try:
                for news in result[1][i]:
                    try:
                        source = news[0]["source"]
                        source_leaning = leaning_ref[leaning[source]]
                        source_fact = fact_ref[fact[source]]
                        # title truncator
                        title = helper_string_trunc(
                            news[0]["description"], 170)
                        tweet_news.append((source, title, news[0]["url"],
                                           source_leaning, news[1], source_fact))
                    except KeyError:
                        title = "This article failed to load."
                        tweet_news.append(("", title, "#",
                                           "", "", ""))
            except KeyError:
                tweet_news.append(("#", "Error: This article failed to load properly.", "#",
                                        "#", "#", "#"))
            news_list.append(tweet_news)
            tw_news_num.append(len(tweet_news))

    except tweepy.TweepError as err:
        print("Oops, something went wrong!")
        if err.reason.find("status code = 404") > -1:
            print("Houston, we got a TweepError 404")
            error_msg = "User \"" + user + \
                "\" either does not exist, or is inactive. Please try another search."
            error.append(error_msg)
            error.append("TweepyError code: 404")
        else:
            error.append(
                "An error occured. Please refresh the page, or try another search.")
            error.append("TweepyError")

    except:
        print("Oops, something went wrong!")
        error.append(
            "An error occured. Please refresh the page, or try another search.")
        try:
            e = sys.exc_info()[0]
            error.append(e)
        except:
            print("Unknown Error")

    time_taken = round(time.time() - start_time, 5)
    if len(error) == 0:
        if len(tw_text) == 0:
            error.append(
                "Your search returned no results, please try searching for something else.")

    return render_template("results.html",
                           user=user, topic=topic, length=length,
                           tw_id_str=tw_id_str, tw_text=tw_text, tw_text_trunc=tw_text_trunc,
                           tw_date=tw_date, tw_retweets=tw_retweets, tw_like=tw_like,
                           tw_user_data=tw_user_data, tw_user_counts=tw_user_counts, tw_user_media_obj=tw_user_media_obj,
                           tw_news_num=tw_news_num, news_list=news_list,
                           error=error, time_taken=time_taken)


@irsystem.route("/trigger_error_404")
def test_error_404():
    return abort(404)


@irsystem.route("/trigger_error_500")
def test_error_500():
    return abort(500)
