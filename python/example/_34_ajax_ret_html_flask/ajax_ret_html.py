
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('input_form.html')

@app.route("/ajax_page", methods=['POST'])
def ajax_page():
	data = request.get_json()
	print(data)
	rdata = {}
	rdata['return']="<b>Hello</b>"
	print(rdata)
	return jsonify(rdata)

if __name__ == "__main__":
	app.run(port=8080, debug=True)

