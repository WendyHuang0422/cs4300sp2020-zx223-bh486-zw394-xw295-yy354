import json
import urllib
from urllib import request


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
    instance = retrieve_news_article(
        N, '8ba8b6889b1343508e1ba0b55849ec31', date1, date2, order, query)
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
