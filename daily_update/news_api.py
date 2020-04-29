from spacy import load
import numpy as np
import math
from nltk.corpus import stopwords
import json
import urllib
from urllib import request
import newspaper
from newspaper import Article
from collections import defaultdict
import pandas as pd
import nltk
import spacy
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')


def raw_news_retrieval(query, api_key, date1, date2, N, page, sort):
    """
    return a json file specified in 
    query: a tuple or a keyword, the tuple should represent

    api_key: the auth key to retrieve the news
    time_span: a string in the format of 'yyyy-mm-dd:yyyy-mm-dd' indicating the
              timespan from the first date to the second one
    """
    # build the url
    sources = "abc-news,cbs-news,associated-press,bloomberg,nbc-news,fox-news,reuters,usa-today,business-insider,the-hill,espn,axios,bbc-news"
    keys_a = "&apiKey=" + api_key
    date_a = '&to='+date2+'&from='+date1
    if not query is None:
        query = 'everything?q='+query + '&'
    else:
        query = 'everything?q='
    url = "https://newsapi.org/v2/"+query\
          + '/page='+str(page)+'&pageSize=' + str(N) + \
        '&sortBy=' + sort + date_a+"&language=en"+"&sources="+sources+keys_a

    agg_file = json.load(urllib.request.urlopen(url))

    return agg_file


results = []


def retrieve_news_article(N, keys, date1, date2, order, query):
    """
    retrieve N top results from the news API pool of news report

    N: the total number of wanted news
    key: the API key for access
    query: the string query terms for the search, can be in the format
     of  "keyword", "keyword AND keyword", "keyword NOT keyword", 
     "keyword OR keyword"
     query (any operator) (query), 
     keyword (any operator) query
     default is None
    date11: the start date of the timespan from which we retrieve news
      format: "yyyy-mm-dd"
    date2: the end date of the time span from which we retrieve news
    order: one of 'pubishedAt', 'relevancy',or 'popularity' 
    """
    # results = []
    date = date1+':'+date2
    results_left = 1
    page = 0

    count = 0
    i = 0
    key = keys[i]
    # instance = raw_news_retrieval(
    #         query, key, date1, date2, 100, page, 'publishedAt')
    # limit = instance['status'] == 'ok'
    limit = True
    retrieved = set()
    while limit == True:
        try:
            key = keys[i]
            instance = raw_news_retrieval(
                query, key, date1, date2, 100, page, 'publishedAt')
            limit = instance['status'] == 'ok'
            for article in instance['articles']:
                if count % 100 == 0:
                    print(count)
                if article['url'] not in retrieved:
                    count += 1
                    results.append(article)
                    retrieved.add(article['url'])
            if len(results) >= N:
                return results[:N]
            page = page + 1
            instance = raw_news_retrieval(
                query, keys[i], date1, date2, 100, page, 'publishedAt')
            limit = instance['status'] == 'ok'
        except:
            print("------=========   heloo ======")
            print(len(results))
            i += 1
            if i == len(keys):
                return results
            pass
            # key = keys[i]
            # instance = raw_news_retrieval(
            #     query, key, date1, date2, 100, page, 'publishedAt')
            # limit = instance['status'] == 'ok'

    print("there are not enoguh results that can be retrieved, returning as many as we can")
    return (results)


def news_Aggregated(N, date1, date2, order, query=None):
    """
    retrieve N top results from the news API pool of news report
    in the format specified in the degin doc (list of news, each represented by
    a dicitonary)

    N: the total number of wanted news
    query: the string query terms for the search, can be in the format
     of  "keyword", "keyword AND keyword", "keyword NOT keyword", 
     "keyword OR keyword"
     query (any operator) (query), 
     keyword (any operator) query
     default is None
    date11: the start date of the timespan from which we retrieve news
      format: "yyyy-mm-dd"
    date2: the end date of the time span from which we retrieve news

    (the time span can at most be one month)

    order: one of 'pubishedAt', 'relevancy',or 'popularity' 

    libraries:
    re
    urllib
    json
    """
    instance = retrieve_news_article(
        N, ["a0c45775a6714e06b7dd975a7757997d", "c33d4fa299fb48548e55d405eb842066", "1c65f25827d745649be0ea2818ca2667",
            "be0df2da3eb84d5eae22ae1c4443f710", "40aa19742fb54d1a806a7c7785068ab1",
            "681b44cc0dea4b3baa66f6e2ecdf7161", "b5a15ccfd37149fbbeec4d9177d163e9"
            "5af3cde7a82f43998721f7a36f69a6be", "58cacb81c6424e4494857fa0de0a422f",
            "3af999d7b5d241429f6c5437e55b0244", "7ae791fb7ff447d4b8b773766d8891f0",
            "7d1aa6b9b6404411959be508a620be08", "c1b13c06d9634e33b015c7174485ea71",
            "20e6fd42ed5c41638ab913765936c2eb",
            "770d3e15e7234b028da0d84fc0fb6210", "faaccca75145413bb1afe5f9742e34be",
            "ac4e23f90a0e40eeb1732a4507f768ed", "9f2590eef62045aead200877ef8e16f1",
            "B8073fe826ee44b48ebf71b767901a43", "7ae791fb7ff447d4b8b773766d8891f0",
            "3ebcb31788484caca0186832bdbbba63", "0ab86b9133554662bd5577593b2a5b50",
            "c34679daedc3459f8192323b82f447c9", "f5e10b46583d48428332c0187049cade"
            ], date1, date2, order, query)
    wanted = ['source', 'author', 'description',
              'publi_time', 'url', 'content']
    full1 = []
    count = 0
    for idx in instance:
        data1 = {x: None for x in wanted}
        data1['source'] = idx['source']['name']
        data1['author'] = idx['author']
        data1['description'] = idx['description']
        data1['publi_time'] = idx['publishedAt']
        data1['url'] = idx['url']
        data1['content'] = idx['content']
        full1.append(data1)
        count += 1
    return full1


def get_news_text(url_list):
    """
      Retreive the news text from the url listm return list of string in the given
      url input order 
      (some url might not be avialble fo this method so the return list might be 
      less than the given url link)
      [text1, text2, ...]

      url_list: a list of urls
      Return: a list of strings(news content)

      Required Library: newspaper3k, nltk
      """
    text_list = []
    for i in range(len(url_list)):
        url = url_list[i]
        article = Article(url)
        try:
            # this sometimes casue error due to bad http requests
            article.download()
            article.parse()
            text_list.append(article.text)
        except:
            text_list.append(" ")
    return text_list


def full_text_integerate(list_dictionaries1):
    """
    use this function to retrieve 1. inverted_index 2.list of dictionaries without text

    returns dicitonaries for 
    1.inverted_index
    2.document norms
    3.idf
    4.list of dictionaries without texts (no 'contents' or 'description' keys)
    """
    print(list_dictionaries1[0])
    list_dictionaries = [dict(ele) for ele in list_dictionaries1]
    urls = [news['url'] for news in list_dictionaries]
    full_text = get_news_text(urls)
    tokenized = []
    for text_idx in range(len(full_text)):
        instance = list_dictionaries[text_idx]
        if full_text[text_idx] is None:
            if len(instance['description']) > len(instance['content']):
                full_text[text_idx] = instance['description']
            else:
                full_text[text_idx] = instance['content']
        del list_dictionaries[text_idx]['description']
        del list_dictionaries[text_idx]['content']
    # tokenized = tokenize_news(
    #     full_text, stemming=False, pos=True, lower=True, remove_stop=True, nltk1=False)
    tokenized = tokenize_news(
        full_text, stemming=False, pos=True, lower=True, remove_stop=True, nltk1=True)
    inverted_index = build_inverted_idx_zw(tokenized)
    idf = compute_idf(inverted_index, len(tokenized),
                      min_df=1, max_df_ratio=0.7)
    inverted_index = {key: val for key,
                      val in inverted_index.items() if key in idf.keys()}
    doc_norms = compute_doc_norms(inverted_index, idf, len(tokenized))

    return inverted_index, doc_norms, idf, list_dictionaries


def build_inverted_idx_zw(tokenized_tweets):
    """
    build inverted index for the list of twitter posts content
    tokenized_tweets: list of tokenized tweets
    return : a dictionary:  {term1: (doc_id, count_of_term1_in_doc), 
                            term2: (doc_id, count_of_term2_in_doc) ... }
    """
    result = defaultdict(lambda: [], {})
    for i in range(len(tokenized_tweets)):
        tweet = tokenized_tweets[i][0]
        sofar = set()
        for tok in tweet:
            if(tok not in sofar):
                result[tok].append((i, tweet.count(tok)))
                sofar.add(tok)
    return result


def compute_idf(inv_idx, n_docs, min_df=1, max_df_ratio=1):
    result = {}
    for word in inv_idx:
        num = len(inv_idx[word])
        if(num >= min_df and num <= max_df_ratio*n_docs):
            result[word] = math.log(n_docs/(1+num), 2)
    return result


def compute_doc_norms(index, idf, n_docs):
    result = [0]*n_docs
    for word in index:
        per = index[word]
        for ind in per:
            if(word in idf):
                result[ind[0]] += (ind[1]*idf[word])**2
    norm = np.sqrt(result)
    temp = {}
    for i in range(len(norm)):
        temp[i] = norm[i]
    return temp


def tokenize_news(news_texts, stemming=False, pos=False, lower=True, remove_stop=True, nltk1=True):
    if stemming and pos:
        stemming = False
    result = []
    stemmer = nltk.PorterStemmer()
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    parse = None
    if not nltk1:
        parser = spacy.load('en_core_web_sm')
    wanted = ['N', 'P', 'J', 'V', 'P']  # 'VB'
    wanted_scp = ['ADJ', 'NOUN', 'VERB', 'PROPN', 'PROPN']
    for news in news_texts:
        sentences = nltk.sent_tokenize(news)
        tokens = []
        for sent in sentences:
            temp = sent
            rich_word = None
            if lower:
                temp = sent.lower()
            if nltk1:
                sent_tok = nltk.word_tokenize(temp)
            if not nltk1:
                rich_word = parser(temp)
                sent_tok = [x.text for x in rich_word]
            sent_tok = tokenizer.tokenize(temp)
            # if pos:
            #     if nltk1:
            #         tags = [x[1] for x in nltk.pos_tag(sent_tok)]
            #         sent_tok = [sent_tok[i] for i in range(
            #             len(sent_tok)) if tags[i][:1] in wanted]
            #     elif not nltk1:
            #         tags = [word.pos_ for word in rich_word]
            #         sent_tok = [sent_tok[i] for i in range(
            #             len(sent_tok)) if tags[i] in wanted_scp]
            if stemming:
                for idx in range(len(sent_tok)):
                    sent_tok[idx] = stemmer.stem(sent_tok[idx])

            if remove_stop:
                stop_words = stopwords.words('english')
                temp = []
                for tok in sent_tok:
                    if tok not in stop_words:
                        temp.append(tok)
                sent_tok = temp

            tokens.extend(sent_tok)
        result.append((tokens, 'padded'))
    return result
