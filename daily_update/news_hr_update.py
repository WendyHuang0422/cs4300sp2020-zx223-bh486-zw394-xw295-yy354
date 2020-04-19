import gardian
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime, timedelta
import json
from gardian import*
from news_api import *


def mongo_store(source_name, dictionary):
    client = pymongo.MongoClient(
        'mongodb://alicia:alicia1@ds139944.mlab.com:39944/heroku_4pflvg1c')
    db = client.get_default_database()

    collection = db[source_name]
    # a = []
    # for i in range(100):
    #     temp = {'a': i, 'weeksAtOne': 100}
    #     a.append(temp)

    document = {"dictionary": dictionary}
    if collection.find_one({}) == None:
        collection.insert_one(document)
    else:
        collection.find_one_and_replace({},  document)
    client.close()


def get_mongo_store(source_name):
    client = pymongo.MongoClient(
        'mongodb://alicia:alicia1@ds139944.mlab.com:39944/heroku_4pflvg1c')
    db = client.get_default_database()

    collection = db[source_name]
    cursor = collection.find_one({})
    print(cursor['dictionary'])
    # for doc in cursor:
    #     print(source_name)
    #     for dictionary in doc['dictionary']:
    #         print(dictionary)
    client.close()
    return cursor['dictionary']


if __name__ == '__main__':
    DURATION = 10
    TODAY = datetime.today().strftime("%Y-%m-%d")
    START_DATE = (datetime.today() -
                  timedelta(days=DURATION)).strftime("%Y-%m-%d")
    N = 100
    # gardian_dict = guardian_aggregated(N, None, START_DATE+"T23:11:39Z", TODAY+"T23:11:39Z")
    news_dict = news_Aggregated(N, START_DATE, TODAY, "popularity")
    inverted_ind = 
    STORE_ITEMS = []
    STORE_ITEMS.append(("news", news_dict))
    STORE_ITEMS.append(("inverted_ind",inverted_ind))
    for (source_name, dictionary) in STORE_ITEMS:
        mongo_store(source_name, dictionary)

        # check if secuss
        get_mongo_store(source_name)