def generate_q(query):
    result = ''
    if type(query) == str:
        # the base case
        return query
    else:
        if query[1] == 0:
            op = '%20NOT%20'
            return '('+op + generate_q(query[0])+')'
        else:
            if query[1] == 1:
                op = '%20AND%20'
            else:
                op = '%20OR%20'
            return '('+generate_q(query[0][0]) + op + generate_q(query[0][1])+')'


def raw_g_retrieval(query, api_key, time_span, N, page):
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
    # build the url
    date = re.split(':', time_span)
    keys_a = "&api-key=" + api_key
    date_a = '&to-date='+date[1]+'&from-date='+date[0]
    if not query is None:
        query = 'search?q='+query + '&'
    else:
        query = 'search?'
    url = "https://content.guardianapis.com/"+query+'show-blocks=all'+'&format=json'\
          + '&page='+str(page)+'&page-size=' + str(N)+date_a+keys_a

    agg_file = json.load(urllib.request.urlopen(url))
    return agg_file


def retrieve_g_article(N, key, query, date1, date2):
    results = []
    date_counter = date2+':'+date2
    start_date = datetime.strptime(date2, '%Y-%m-%d')
    end_date = datetime.strptime(date1, '%Y-%m-%d')
    while len(results) < N and start_date >= end_date:
        instance = raw_g_retrieval(query, key, date_counter, 200)
        for idx in instance['response']['results']:
            if idx['type'] == 'article':
                results.append(idx)
                if len(results) == N:
                    break
        start_date = start_date - timedelta(days=1)
        new_date = start_date.strftime("%Y-%m-%d")
        date_counter = new_date+':'+new_date
    return results


def retrieve_g_article1(N, key, query, date1, date2):
    results = []
    date = date1+':'+date2
    page_left = 1
    page = 1
    while page_left != 0:
        instance = raw_g_retrieval(query, key, date, 200, page)

        pageSize = instance['response']['pageSize']
        if pageSize < page:
            return results
        currentPage = instance['response']['currentPage']
        for idx in instance['response']['results']:
            if idx['type'] == 'article':
                results.append(idx)
                if len(results) >= N:
                    return results

        page_left = pageSize-currentPage
        page = page + 1


def guardian_aggregated(N, query, date1, date2):
    key = "7dd62f93-de59-4cb6-a166-e7c44543477d"
    raw_jsons = retrieve_g_article1(N, key, query, date1, date2)
    wanted = ['webPublicationDate', 'webTitle', 'webUrl', ]
    order = ['blocks']
    result = []
    for instance in raw_jsons:
        temp = {}
        for key in wanted:
            temp[key] = instance[key]
        if(len(instance['blocks']['body'][0]['bodyTextSummary']) > 0):
            temp['text'] = instance['blocks']['body'][0]['bodyTextSummary']
        else:
            temp['text'] = instance['blocks']['body'][0]['bodyHtml']

        result.append(temp)
    return result
