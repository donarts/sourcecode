from flask import Flask, make_response, jsonify, request

stock = {
	"fruit": {
		"apple": 10,
		"banana": 20
	}
}

app = Flask(__name__)

@app.route("/stock")
def get_stock():
	res = make_response(jsonify(stock), 200)
	return res
 
@app.route("/stock/<goods>")
def get_goods(goods):
	""" Returns a goods from stock """
	if goods in stock:
		res = make_response(jsonify(stock[goods]), 200)
		return res
	res = res = make_response(jsonify({"error": "Not found"}), 404)
	return res

@app.route("/stock/<goods>", methods=["POST"])
def create_goods(goods):
	""" Creates a new goods if it doesn't exist """
	req = request.get_data()
	print("create_goods")
	print(req)
	res = make_response(jsonify({"message": "goods created"}), 201)
	return res

if __name__ == '__main__':
	app.run(debug=True)
