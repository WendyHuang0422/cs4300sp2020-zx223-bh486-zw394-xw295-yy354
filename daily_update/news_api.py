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
    keys_a = "&apiKey=" + api_key
    date_a = '&to='+date2+'&from='+date1
    if not query is None:
        query = 'everything?q='+query + '&'
    else:
        query = 'everything?q='
    url = "https://newsapi.org/v2/"+query\
          + '/page='+str(page)+'&pageSize=' + str(N) + \
        '&sortBy=' + sort + date_a+keys_a

    agg_file = json.load(urllib.request.urlopen(url))

    return agg_file


def retrieve_news_article(N, key, date1, date2, order, query):
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
    results = []
    date = date1+':'+date2
    results_left = 1
    page = 0
    while results_left != 0:
        instance = raw_news_retrieval(
            query, key, date1, date2, 100, page, 'publishedAt')
        totalSize = instance['totalResults']
        results.extend(instance['articles'])
        results_left = totalSize-len(results)
        if len(results) >= N:
            return results[:N]
        page = page + 1
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
    print("news_api using  N is  ", N)
    instance = retrieve_news_article(
        N, '770d3e15e7234b028da0d84fc0fb6210', date1, date2, order, query)
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
    print("count is ***************", count)
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
