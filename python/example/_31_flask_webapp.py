from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
	inputdata = request.args.get("inputdata", "")
	if inputdata:
		result = calc(inputdata)
	else:
		result = ""
	return (
		"""<form action="" method="get">
				Calc : <input type="text" name="inputdata">
				<input type="submit" value="calc">
			</form>"""
		+ "result:" + result
	)

def calc(inputdata):
	return str(eval(inputdata))

if __name__ == "__main__":
	app.run(port=8080, debug=True)

