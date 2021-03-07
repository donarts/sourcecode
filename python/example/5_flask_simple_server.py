from flask import Flask, json

funs = [{"id": 1, "name": "fun1"}, {"id": 2, "name": "fun2"}]

api = Flask(__name__)

@api.route('/funs', methods=['GET'])
def get_funs():
  return json.dumps(funs), 200

@api.route('/funs', methods=['POST'])
def post_funs():
  return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run(debug=True)