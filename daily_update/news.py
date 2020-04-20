import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime, timedelta
import json
from news_api import *
import sys


def mongo_store(source_name, dictionary):
    client = pymongo.MongoClient(
        'mongodb://alicia:alicia1@ds139944.mlab.com:39944/heroku_4pflvg1c')
    db = client.get_default_database()

    collection = db[source_name]

    print("-------------  helooooo  ---------------")

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
    N = int(sys.argv[1])
    # N = 3
    # gardian_dict = guardian_aggregated(N, None, START_DATE+"T23:11:39Z", TODAY+"T23:11:39Z")

    news_dict = news_Aggregated(N, START_DATE, TODAY, "pubishedAt")
    inverted_index, document_norms, idf, dictionaries_without_texts = full_text_integerate(
        news_dict)
    document_norms = {str(key): document_norms[key] for key in document_norms}

    STORE_ITEMS = []
    # print('.' in inverted_index)

    STORE_ITEMS.append(("news", news_dict))
    STORE_ITEMS.append(("inverted_index", inverted_index))
    STORE_ITEMS.append(("document_norms", document_norms))
    STORE_ITEMS.append(("idf", idf))
    STORE_ITEMS.append(("dictionaries_without_texts",
                        dictionaries_without_texts))
    for (source_name, dictionary) in STORE_ITEMS:
        mongo_store(source_name, dictionary)

        # check if secuss
        get_mongo_store(source_name)
