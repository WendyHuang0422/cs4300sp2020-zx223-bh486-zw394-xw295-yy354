from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Tweeted Facts"
net_id = "Zenong Wang: zw394, Wendy Huang: bh486, Alicia Yang: yy354, " \
		 "Zi Heng Xu: zx223, Iris Wang: zw295"

@irsystem.route("/", methods=['GET'])
def search():
	query = request.args.get('search')
	keywords = request.args.get('terms', None)
	if not query:
		data = []
		user = ''
		topic = ""
	else:
		user = query
		if not keywords:
			topic = ""
		else:
			topic = keywords
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, user=user, data=data, topic=topic)
