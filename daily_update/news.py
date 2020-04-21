import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime, timedelta
import json
from news_api import *
import sys
import csv


def mongo_store(source_name, dictionary):
    client = pymongo.MongoClient(
        'mongodb://alicia:alicia1@ds139944.mlab.com:39944/heroku_4pflvg1c')
    db = client.get_default_database()

    collection = db[source_name]
    print("source_name")

    print("-------------  helooooo  ---------------")

    document = {"dictionary": dictionary}
    if source_name == "inverted_index1":
        keys = dictionary.keys()
        with open('./inverted_index.csv', 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            document = {"dictionary": pd.DataFrame.from_dict(data=dictionary, orient='index').to_csv(
                'dict_file.csv', header=False)}
            # for key, value in dictionary.items():
            #     dict_writer.writerow([key, value])
            # dict_writer.writeheader()
            # dict_writer.writerows(dictionary)

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
    result = cursor['dictionary']
    if source_name == "inverted_index1":
        print("gooooooooddddd   ******")
        print(result)
        # data = pd.read_csv(result)
        # result = {col: list(data[col]) for col in data.columns}

    client.close()
    return result


if __name__ == '__main__':
    DURATION = 10
    TODAY = datetime.today().strftime("%Y-%m-%d")
    START_DATE = (datetime.today() -
                  timedelta(days=DURATION)).strftime("%Y-%m-%d")
    N = int(sys.argv[1])
    # N = 2
    # gardian_dict = guardian_aggregated(N, None, START_DATE+"T23:11:39Z", TODAY+"T23:11:39Z")

    news_dict = news_Aggregated(N, START_DATE, TODAY, "pubishedAt")
    # news_dict = get_mongo_store('news')
    inverted_index, document_norms, idf, dictionaries_without_texts = full_text_integerate(
        news_dict)
    document_norms = {str(key): document_norms[key] for key in document_norms}
    print("------   finished computation now start storing   ------")

    STORE_ITEMS = []
    # print('.' in inverted_index)
    i = ''
    STORE_ITEMS.append(("news"+i, news_dict))
    STORE_ITEMS.append(("inverted_index"+i, inverted_index))
    STORE_ITEMS.append(("document_norms"+i, document_norms))
    STORE_ITEMS.append(("idf"+i, idf))
    STORE_ITEMS.append(("dictionaries_without_texts"+i,
                        dictionaries_without_texts))
    for (source_name, dictionary) in STORE_ITEMS:
        mongo_store(source_name, dictionary)

        # check if secuss
        get_mongo_store(source_name)
