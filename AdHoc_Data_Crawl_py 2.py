#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/WendyHuang0422/cs4300sp2020-zx223-bh486-zw394-xw295-yy354/blob/master/AdHoc_Data_Crawl.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[ ]:


def create_ApI(consumer_key,s_consmer_key,access_key,s_acess_key):
  #given the authroization return a tweepy api object for retrieving data
  auth = tweepy.OAuthHandler(consumer_key, s_consmer_key)
  auth.set_access_token(access_key, s_acess_key)
  api = tweepy.API(auth)
  return api

def tweet_score(status,timeline):
  """
  the current version assign score simply by the time-stamp
  the greater the score assigned is, the more relevant it is
  status: the particular status that we want to assign a score to
  timeline: the entire list of retrieved status
  """
  time = [int(x) for x in list(filter(None,re.split('[\s:-]',str(status.created_at))))]
  score = (time[0]-2000)*120 + time[1]*10 + time[2] + time[3]/12
  return score

def retrieve_tweets(N,celeb_name,inc_retweets,api):
  """
  help to retrieve the needed number of tweets beyond the number 20
  this function does not assigne scores to each tweets
  N: the number of wanted tweets
  celeb_name: the screen name of the celebrity
  inc_retweets: a boolean varibale indicating whether retweets
                are going to be included
  """
  if inc_retweets:
    return list(api.user_timeline(screen_name = celeb_name,count = N))

  pool = list(api.user_timeline(screen_name = celeb_name,count = 2*N))
  result = []
  count = 0
  while count<20: 
    for status in pool[:-1]:
      if not hasattr(status,'retweeted_status'):
        result.append(status)
      if len(result) == N:
        return result
    last = pool[-1].id
    pool = list(api.user_timeline(screen_name = celeb_name,count = 2*N,                                  since_id = 1,max_id=last))
    count += 1
  return (None,'the user made no recent tweets, try include retweets')


def tweets_crawl(N,pool_size,celeb_name,api,inc_retweets):
  """ 
    retrieve the top N tweets tweeted by the celeb_account
    N: the number of wnated accounts

    celeb_name: a string, the screen_name of the celebrity
    api: the tweepy api object
    pool_size: the size of the pool of potential tweets from which we retrieve
      N most significant
    inc_retweets: whether we include retweets, set to False to retrieve only
    original tweets
  """
  timeline = retrieve_tweets(pool_size,celeb_name,inc_retweets,api)
  if timeline[0] is None:
    print(timeline[1])
    return
  sorted_timeline = []
  for status in timeline:
    score = tweet_score(status,timeline)
    sorted_timeline.append((status,score))
  sorted_timeline = sorted(sorted_timeline,key=lambda x:x[1],reverse = True)
  return sorted_timeline[:N]


def twittter_aggregated(N,pool_size,celeb_name,inc_retweets):
  """
  the aggregated retrieval function  to retrieve N most recent tweets from pool_size
  potential tweets, for example, 200 tweets from 400 tweets in the format
  specified in the google doc (a list of dictionaries with each dictionary
  representing a tweet). 
  Call this function in the other stages of the system

  READ: this function depends on 
  tweepy
  math
  urllib
  json
  import these modules before calling

  N: the number of wnated accounts

  celeb_name: a string, the screen_name of the celebrity
  api: the tweepy api object
  pool_size: the size of the pool of potential tweets from which we retrieve
    N most significant
  inc_retweets: whether we include retweets, set to False to retrieve only
    original tweets
  """
  
  c_key = '4xQ7FcDfGAlAM5JkG505ndS3k'
  s_c_key = 'GJkKVtF34AoqaXSdCXq6agxCKrj1T2FL9i2w28Yj9t2wCo6jmM'
  a_key =  '1247186585994637312-6ZuAFM9bhsv1Mil7utLrL0stxbT8ft'
  s_a_key = 'PkPrIdOOPSoQwCM0TuKF4dqLiKOOdTemEpjh2Ewf44FUd'
  api =  create_ApI(c_key,s_c_key,a_key,s_a_key)
  user = api.get_user(screen_name='realDonaldTrump')
  data = []


  wanted = ['text','created_at','id','retweet_count','favorite_count']
  count = 0
  recent = tweets_crawl(N,pool_size,celeb_name,api,inc_retweets)
  print(recent[-1])
  for idx in recent:
    idx = idx[0]._json
    temp = {x:idx[x] for x in wanted}
    data.append(temp)
  return data






# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
#all these keys should go into a json (or the provided secrect environment file
#later for secrecy

guardian_key = '7dd62f93-de59-4cb6-a166-e7c44543477d'




#with open('/content/drive/My Drive/Twitter_Account.txt',"w") as outfile:
  #json.dump(data,outfile)


# Bing API

# In[ ]:




def raw_news_retrieval(query,api_key,date1,date2,N,page,sort):
  """
  return a json file specified in 
  query: a tuple or a keyword, the tuple should represent
        
  api_key: the auth key to retrieve the news
  time_span: a string in the format of 'yyyy-mm-dd:yyyy-mm-dd' indicating the
            timespan from the first date to the second one
  """
  #build the url
  keys_a = "&apiKey=" + api_key
  date_a = '&to='+date2+'&from='+date1
  if not query is None:
    query = 'everything?q='+query + '&'
  else:
    query = 'everything?q='
  url = "https://newsapi.org/v2/"+query        +'page='+str(page)+'&pageSize=' +str(N)+'&sortBy='+ sort +date_a+keys_a

  agg_file = json.load(urllib.request.urlopen(url))
 
  return agg_file


def retrieve_news_article(N,key,date1,date2,order,query):
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
    instance = raw_news_retrieval(query,key,date1,date2,100,page,'publishedAt')
    totalSize = instance['totalResults']
    results.extend(instance['articles'])
    results_left = totalSize-len(results)
    if len(results) >= N:
      return results[:N]
    page = page + 1  
  print("there are not enoguh results that can be retrieved, returning as many as we can")
  return (results)



def news_Aggregated(N,date1,date2,order,query=None):
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
  instance = retrieve_news_article(N,'8ba8b6889b1343508e1ba0b55849ec31',date1,date2,order,query)
  wanted = ['source','author','description','publi_time','url','content']
  full1 = []
  count = 0
  for idx in instance:
    data1 = {x:None for x in wanted}
    data1['source'] = idx['source']['name']
    data1['author'] = idx['author']
    data1['description'] = idx['description']
    data1['publi_time'] = idx['publishedAt']
    data1['url'] = idx['url']
    data1['content'] = idx['content']
    full1.append(data1)
    count += 1
  return full1


# In[ ]:


def bing_retrieve_raw(N,query,key):
  """
  retrieve API results from Bing News API specified under
  https://docs.microsoft.com/en-us/rest/api/cognitiveservices-bingsearch/bing-news-api-v7-reference

  N: the number of results wanted
  query: the search keywords
  
  """
  #Bing API
  search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
  headers = {"Ocp-Apim-Subscription-Key" : key}
  q = ''
  if not query is None:
    q = query
  params  = {"q": q, 'count':100,'offset':1,'mkt':'en-US'}
  response = requests.get(search_url, headers=headers, params=params)
  response.raise_for_status()
  search_results = response.json()

  # while collected != N:
  #   return search_results


# In[ ]:


import requests
wanted = ['id','is_video','num_comments','permalink','score','title','selftext','preview','url','domain']
bing_key = '3903dc2afaba49208df3bcb91206fe22'
exp = bing_retrieve_raw(1000,None,bing_key)


# In[ ]:


print(exp['value'][2]['description'])


# Codes for Reddit API, now abandoned 

# In[ ]:




def reddit_sub_retrieve(N,query,date1,date2):
  """
  https://pushshift.io/api-parameters/
  thanks pushshift
  """
  url = "https://api.pushshift.io/reddit/submission/search/?"
  query_t = ''
  if query != None:
    query_t = 'q=' + query + '&'
  date1_e = 'after'+ str(datetime.strptime(date1,'%Y-%m-%d-%H-%S').timestamp())
  date2_e = '&before'+ str(datetime.strptime(date2,'%Y-%m-%d-%H-%S').timestamp())
  url = url + query_t + date1_e + date2_e + '&subreddit=news'
  agg_file = json.load(urllib.request.urlopen(url))
  return agg_file

instance = reddit_sub_retrieve(0,None,'2020-04-09-11-05','2020-04-10-12-05')


# In[ ]:


print(full1[-1])


# Plotting

# In[ ]:


average_length1 = {}
average_length2 = {}
length1 = 0
length2 = 0
for ins in full1:
  old1 = average_length1.get(ins['source'],(0,0))
  old2 = average_length2.get(ins['source'],(0,0))
  average_length1[ins['source']] = (old1[0]+len(ins['description']),old1[1]+1)
  if ins['content'] is not None:
    average_length2[ins['source']] = (old2[0]+len(ins['content']),old2[1]+1)
    length2 += len(ins['content'])
  else:
    average_length2[ins['source']] = (old2[0]+0,old2[1]+1)
    length2 += 0
  length1 += len(ins['description'])

for keys in average_length1.keys():
  average_length1[keys] = (average_length1[keys][0]/average_length1[keys][1],average_length1[keys][1])
  average_length2[keys] = (average_length2[keys][0]/average_length2[keys][1],average_length1[keys][1])
length1 = length1/len(full1)
length2 = length2/len(full1)

print(length1)
print(length2)
print(average_length1)
print(average_length2)


# In[ ]:


import matplotlib.pyplot as plt

des = []
content = []
x_label = []
for keys in average_length1.keys():
  des.append(average_length1[keys][0])
  content.append(average_length2[keys][0])
  x_label.append(average_length1[keys][1])


print(x_label)
print(content)

plt.plot(x_label,des, '.k')
plt.plot(x_label,content, '.r')
plt.grid()

plt.show()


# 
# 
# 
# 
# 
# 
# 
# 
# Guardian

# In[ ]:




def generate_q(query):
  result = ''
  if type(query) == str:
    #the base case
    return query
  else:
    if query[1] == 0:
      op = '%20NOT%20'
      return '('+op + generate_q(query[0])+')'
    else:
      if query[1] == 1:
        op =  '%20AND%20'
      else:
        op =  '%20OR%20'
      return '('+generate_q(query[0][0]) + op + generate_q(query[0][1])+')'

def raw_g_retrieval(query,api_key,time_span,N,page):
  """
  return a json file specified in https://open-platform.theguardian.com/documentation/search
  query: a tuple or a keyword, the tuple should represent
        a relation
        ((a,b),1) -> a and b
        ((a,b),2) -> a or b
        ((a,(b,0)),1) -> a and NOT b
        (((a,b),1),(((c,d),2),0),1) = (a AND B) AND NOT (c OR d)
        means reddit AND NOT news AND (random or guardian)
  api_key: the auth key to retrieve the news
  time_span: a string in the format of 'yyyy-mm-dd:yyyy-mm-dd' indicating the
            timespan from the first date to the second one
  """
  #build the url
  date = re.split(':',time_span)
  keys_a = "&api-key=" + api_key
  date_a = '&to-date='+date[1]+'&from-date='+date[0]
  if not query is None:
    query = 'search?q='+generate_q(query) + '&'
  else:
    query = 'search?'
  url = "https://content.guardianapis.com/"+query+'show-blocks=all'+'&format=json'        +'&page='+str(page)+'&page-size=' +str(N)+date_a+keys_a

  agg_file = json.load(urllib.request.urlopen(url))
  return agg_file


def retrieve_g_article(N,key,query,date1,date2):
  results = []
  date_counter = date2+':'+date2
  start_date = datetime.strptime(date2,'%Y-%m-%d')
  end_date = datetime.strptime(date1,'%Y-%m-%d')
  while len(results)<N and start_date>=end_date:
    instance = raw_g_retrieval(query,key,date_counter,200)
    for idx in instance['response']['results']:
      if idx['type'] == 'article':
        results.append(idx)
        if len(results) == N:
          break
    start_date = start_date - timedelta(days=1)
    new_date = start_date.strftime("%Y-%m-%d")
    date_counter =  new_date+':'+new_date
  return results

def retrieve_g_article1(N,key,query,date1,date2):
  results = []
  date = date1+':'+date2
  page_left = 1
  page = 1
  while page_left != 0:
    instance = raw_g_retrieval(query,key,date,200,page)
    
    pageSize = instance['response']['pageSize']
    currentPage = instance['response']['currentPage']
    for idx in instance['response']['results']:
      if idx['type'] == 'article':
        results.append(idx)
        if len(results) == N:
          return results 
    
    page_left = pageSize-currentPage
    page = page + 1 


# In[ ]:


import tweepy
import math
import re
import urllib
import json
from datetime import datetime
from dateutil.parser import parse
from datetime import timedelta
import sys

start = datetime.now()
instance = retrieve_g_article1(2000,'7dd62f93-de59-4cb6-a166-e7c44543477d',None,'2020-01-01','2020-04-05')
print(instance[0])
wanted = ['sectionName','webTitle','content','publi_time','url']
full = []
count = 0
for idx in instance:
  data = {x:None for x in wanted}
  data['sectionName'] = idx['sectionName']
  data['webTitle'] = idx['webTitle']
  data['publi_time'] = idx['webPublicationDate']
  data['content'] = idx['blocks']['body'][0]['bodyTextSummary']
  data['url'] = idx['webUrl']
  full.append(data)
  count += 1

print(datetime.now()-start)
with open('/content/drive/My Drive/Guardian_News.txt',"w") as outfile:
  json.dump(full,outfile)


# In[ ]:


list0 = []
for ins in full:
  list0.append(len(ins['content']))


# In[ ]:


import matplotlib.pyplot as plt


print(max(list0))


plt.hist(list0)
plt.grid()

plt.show()


# In[ ]:




