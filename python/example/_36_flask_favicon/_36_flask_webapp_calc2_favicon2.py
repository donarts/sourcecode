import os
from flask import send_from_directory
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('input_form.html')

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
	return str(eval(inputdata))

if __name__ == "__main__":
	app.run(port=8080, debug=True)

