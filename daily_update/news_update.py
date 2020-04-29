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


def update_news(N=50):
    """
    N:  total number of pages for update 
    """
    past_news = get_mongo_store("news")
    date2 = datetime.today().strftime("%Y-%m-%d")
    DURATION = 1
    date1 = (datetime.today() -
             timedelta(days=DURATION)).strftime("%Y-%m-%d")
    # date1 = past_news[0]['publi_time']
    date = date1+':'+date2
    keys = [
        "3ebcb31788484caca0186832bdbbba63", "0ab86b9133554662bd5577593b2a5b50",
        "c34679daedc3459f8192323b82f447c9", "f5e10b46583d48428332c0187049cade"]

    news_count = 0
    page = 0
    results_left = 1
    i = 0
    limit = True
    retrieved = set([new['url'] for new in past_news])
    results = []
    while (page < N):
        try:
            if limit != True:
                break
            key = keys[i]
            instance = raw_news_retrieval(
                None, key, date1, date2, 100, page, 'publishedAt')
            limit = instance['status'] == 'ok'
            for article in instance['articles']:
                if article['url'] not in retrieved:
                    news_count += 1
                    results.append(article)
                    retrieved.add(article['url'])
            page = page + 1
        except:
            print("------=========   heloo ======     -----")
            print(len(results))
            i += 1
            if i == len(keys):
                break
            pass

    wanted = ['source', 'author', 'description',
              'publi_time', 'url', 'content']
    full1 = []
    count = 0
    for idx in results:
        data1 = {x: None for x in wanted}
        data1['source'] = idx['source']['name']
        data1['author'] = idx['author']
        data1['description'] = idx['description']
        data1['publi_time'] = idx['publishedAt']
        data1['url'] = idx['url']
        data1['content'] = idx['content']
        full1.append(data1)
        count += 1
    news_dict = full1 + past_news[:(-news_count)]
    return news_dict


def update_full_text(news):
    inverted_index, document_norms, idf, dictionaries_without_texts = full_text_integerate(
        news)
    return inverted_index, document_norms, idf, dictionaries_without_texts


if __name__ == '__main__':

  # INITIAL NEWS RETRIEVAL
    # DURATION = 35
    # TODAY = datetime.today().strftime("%Y-%m-%d")
    # START_DATE = (datetime.today() -
    #               timedelta(days=DURATION)).strftime("%Y-%m-%d")
    # N = int(sys.argv[1])
    # # N = 1500
    # print(N)

    # news_dict = news_Aggregated(N, START_DATE, TODAY, "pubishedAt")
    # inverted_index, document_norms, idf, dictionaries_without_texts = full_text_integerate(
    #     news_dict)
    # print("herere")
    # main(news_dict, inverted_index, document_norms,
    #      idf, dictionaries_without_texts)

  # UPDATING DAILY NEWS
    updated_news = update_news(N=1)
    up_inverted_index, up_document_norms, up_idf, up_dictionaries_without_texts = update_full_text(
        updated_news)
    print(len(update_news))
    print(len(up_inverted_index) == len(up_idf))
    # main(updated_news, up_inverted_index, up_document_norms,
    #      up_idf, up_dictionaries_without_texts)
