from flask import Flask, json, request

funs1 = [{"id": 1, "name": "fun1"}, {"id": 2, "name": "fun2"}]
funs2 = [{"id": 3, "name": "fun1"}, {"id": 4, "name": "fun2"}]

api = Flask(__name__)

@api.route('/funs', methods=['GET'])
def get_funs():
	print("get request.args:",request.args.to_dict())
	print("get request.json:",request.json)
	print("get request.form:",request.form.to_dict())
	print("get request.getdata:",request.get_data())
	return json.dumps(funs1), 200

@api.route('/funs', methods=['POST'])
def post_funs():
	print("post request.args:",request.args.to_dict())
	print("post request.json:",request.json)
	print("post request.form:",request.form.to_dict())
	print("post request.getdata:",request.get_data())
	return json.dumps(funs2), 201

if __name__ == '__main__':
    api.run(debug=True)
