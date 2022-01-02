import time
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('input_form_loading.html')

@app.route("/ajax_page", methods=['POST'])
def ajax_page():
	data = request.get_json()
	print(data)
	calc_result = calc(data['inputdata'])
	rdata = {}
	rdata['inputdata']=data['inputdata']
	rdata['rlt']=calc_result
	print(rdata)
	return jsonify(rdata)

def calc(inputdata):
	print("calc")
	time.sleep(10)
	return str(eval(inputdata))

if __name__ == "__main__":
	app.run(port=8080, debug=True)

