
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('button1.html')

@app.route("/ajax_page", methods=['POST'])
def ajax_page():
	data = request.get_json()
	print(data)
	rdata = {}
	rdata['return']='<input type="text" id="txt2" name="inputdata"></input><button id="btn2">real submit</button>'
	print(rdata)
	return jsonify(rdata)

@app.route("/ajax_page2", methods=['POST'])
def ajax_page2():
	data = request.get_json()
	print(data)
	rdata = {}
	rdata['return']="</b>Hello</b>"
	print(rdata)
	return jsonify(rdata)
	
if __name__ == "__main__":
	app.run(port=8080, debug=True)

