from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from flask import request, jsonify

from app import db
from app.accounts.models.search_terms import Search_terms, Search_users, Tweet_checks
from flask_sqlalchemy import SQLAlchemy

project_name = "Tweeted Facts"
net_id = "Zenong Wang: zw394, Wendy Huang: bh486, Alicia Yang: yy354, " \
		 "Zi Heng Xu: zx223, Iris Wang: zw295"

@irsystem.route("/", methods=['GET', 'POST'])
def search():
	query = request.args.get('search')
	keywords = request.args.get('terms', None)
	user_ip = request.remote_addr
	if not query:
		data = []
		counts = []
		user = ''
		topic = ""
		count_1 = 0
		count_2 = 0
		count_3 = 0
	else:
		user = query
		if not keywords:
			topic = ""
			data = ["Tweet by " + query + " " + str(i) for i in range(5)]
		else:
			topic = keywords
			data = ["Tweet by " + query + " containing \"" + topic + "\" no. " + str(i + 1) for i in range(5)]
		counts = [(Tweet_checks.query.filter(Tweet_checks.combined_str.contains(
			user_ip + ":" + tweet))).count() for tweet in data]
		# for tweet in data:
		# 	if (Tweet_checks.query.filter(Tweet_checks.combined_str.contains(tweet))).count() < 1:

		# 		db.session.add(tweet_data)
		# 		db.session.commit()
		ip_user_query = user_ip + ":</>" + user + "</>"
		ip_terms_query = user_ip + ":</>" + topic + "</>"
		combined_query = user + "<u:t>" + topic + "</>"
		ip_combined_query = user_ip + ":</>" + combined_query
		if (Search_terms.query.filter(Search_terms.combined_query.contains(ip_combined_query))).count() < 1:
			search_data = Search_terms(user_ip = user_ip, user_query = ip_user_query, terms_query = ip_terms_query,
				combined_query = ip_combined_query)
			db.session.add(search_data)
			db.session.commit()
		if (Search_users.query.filter(Search_users.user_query.contains(ip_user_query))).count() < 1:
			search_user_data = Search_users(user_ip = user_ip, user_query = ip_user_query)
			db.session.add(search_user_data)
			db.session.commit()
		count_1 = (Search_users.query.filter(Search_users.user_query.contains(":</>" + query + "</>"))).count()
		count_2 = (Search_terms.query.filter(Search_terms.terms_query.contains(":</>" + keywords + "</>"))).count()
		count_3 = (Search_terms.query.filter(Search_terms.combined_query.contains("<u:t>" + combined_query + "</>"))).count()

	return render_template('search.html', name=project_name, netid=net_id, user=user, data=data, counts=counts,
		topic=topic, count_1=count_1, count_2 = count_2, count_3 = count_3, user_ip = user_ip)

# @irsystem.route("/get_my_ip", methods=["GET"])
# def get_my_ip():
#     return jsonify({'ip': request.remote_addr, "remote_ip": request.environ.get('HTTP_X_REAL_IP', request.remote_addr)   
# }), 200