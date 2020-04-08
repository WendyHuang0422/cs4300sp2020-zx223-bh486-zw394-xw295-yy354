from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from flask import request, jsonify

from app import db
from app.accounts.models.search_terms import Search_terms
from flask_sqlalchemy import SQLAlchemy

project_name = "Tweeted Facts"
net_id = "Zenong Wang: zw394, Wendy Huang: bh486, Alicia Yang: yy354, " \
		 "Zi Heng Xu: zx223, Iris Wang: zw295"

@irsystem.route("/", methods=['GET', 'POST'])
def search():
	query = request.args.get('search')
	keywords = request.args.get('terms', None)
	if not query:
		data = []
		user = ''
		topic = ""
		count = 0
	else:
		user = query
		if not keywords:
			topic = ""
		else:
			topic = keywords
		data = range(5)
		count = (Search_terms.query.filter(Search_terms.user_query.contains(query))).count()
	user_ip = request.remote_addr
	search_data = Search_terms(user_query = user, terms_query = topic)
	db.session.add(search_data)
	db.session.commit()

	return render_template('search.html', name=project_name, netid=net_id, user=user, data=data, 
		topic=topic, count=count, user_ip = user_ip)

@irsystem.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr, "remote_ip": request.environ.get('HTTP_X_REAL_IP', request.remote_addr)   
}), 200