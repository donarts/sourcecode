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
	req = request.get_json()
	if goods in stock:
		res = make_response(jsonify({"error": "goods already exists"}), 400)
		return res
	stock.update({goods: req})
	res = make_response(jsonify({"message": "goods created"}), 201)
	return res
	
@app.route("/stock/<goods>", methods=["PUT"])
def put_goods(goods):
	""" Replaces or creates a goods """
	req = request.get_json()
	if goods in stock:
		stock[goods] = req
		res = make_response(jsonify({"message": "goods replaced"}), 200)
		return res
	stock[goods] = req
	res = make_response(jsonify({"message": "goods created"}), 201)
	return res
 
@app.route("/stock/<goods>", methods=["PATCH"])
def patch_goods(goods):
	""" Updates or creates a goods """
	req = request.get_json()
	if goods in stock:
		for k, v in req.items():
			stock[goods][k] = v
		res = make_response(jsonify({"message": "goods updated"}), 200)
		return res
	stock[goods] = req
	res = make_response(jsonify({"message": "goods created"}), 201)
	return res

@app.route("/stock/<goods>", methods=["DELETE"])
def delete_goods(goods):
	""" If the goods exists, delete it """
	if goods in stock:
		del stock[goods]
		res = make_response(jsonify({}), 204)
		return res

	res = make_response(jsonify({"error": "goods not found"}), 404)
	return res

if __name__ == '__main__':
	app.run(debug=True)
