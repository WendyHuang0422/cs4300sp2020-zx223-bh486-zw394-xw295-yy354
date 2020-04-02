from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Tweeted Facts"
net_id = "Zenong Wang: zw394, Wendy Huang: bh486, Alicia Yang: yy354, " \
		 "Zi Heng Xu: zx223, Iris Wang: zw295"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



