import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime, timedelta
import json
from news_api import *
import sys
import csv


def mongo_store(source_name, dictionary, frac=6):
    client = pymongo.MongoClient(
        'mongodb://alicia:alicia1@ds139019-a0.mlab.com:39019,ds139019-a1.mlab.com:39019/heroku_gczdn597?replicaSet=rs-ds139019&retryWrites=false')
    db = client.get_default_database()

    print(source_name)

    print("-------------  helooooo  ---------------")

    if source_name == "inverted_index":
        start = 0
        listofDict = list(dictionary.items())
        ranges = [int(len(dictionary)*(i)/frac) for i in range(frac+1)]
        start = 0
        for i in range(frac):
            collection = db[source_name+str(i)]
            end = ranges[i+1]
            res = dict(listofDict[start:end])
            document = {"dictionary": res}
            if collection.find_one({}) == None:
                collection.insert_one(document)
            else:
                collection.find_one_and_replace({},  document)
            start = end
    else:
        collection = db[source_name]
        document = {"dictionary": dictionary}
        if collection.find_one({}) == None:
            collection.insert_one(document)
        else:
            collection.find_one_and_replace({},  document)
    client.close()


"""
Please copy this function if you want to get the mongo store elements
"""


def get_mongo_store(source_name, frac=6):
    client = pymongo.MongoClient(
        'mongodb://alicia:alicia1@ds139019-a0.mlab.com:39019,ds139019-a1.mlab.com:39019/heroku_gczdn597?replicaSet=rs-ds139019')
    db = client.get_default_database()
    result = {}
    if source_name == "inverted_index":
        for i in range(frac):
            collection = db[source_name+str(i)]
            cursor = collection.find_one({})
            result.update(cursor['dictionary'])
    else:
        collection = db[source_name]
        cursor = collection.find_one({})
        result = cursor['dictionary']
    # print(result)

    client.close()
    return result


def main(news_dict, inverted_index, document_norms, idf, dictionaries_without_texts):
    document_norms = {str(key): document_norms[key] for key in document_norms}
    print("------   finished computation now start storing   ------")

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
        # get_mongo_store(source_name)


def daily_update():
    updated_news = update_news(total=1500, N=200)
    up_inverted_index, up_document_norms, up_idf, up_dictionaries_without_texts = update_full_text(
        updated_news)
    main(updated_news, up_inverted_index, up_document_norms,
         up_idf, up_dictionaries_without_texts)


if __name__ == '__main__':
    DURATION = 35
    TODAY = datetime.today().strftime("%Y-%m-%d")
    START_DATE = (datetime.today() -
                  timedelta(days=DURATION)).strftime("%Y-%m-%d")
    N = int(sys.argv[1])
    # N = 1500
    print(N)

    news_dict = news_Aggregated(N, START_DATE, TODAY, "pubishedAt")
    inverted_index, document_norms, idf, dictionaries_without_texts = full_text_integerate(
        news_dict)
    print("finished tf idf computation")
    main(news_dict, inverted_index, document_norms,
         idf, dictionaries_without_texts)
