from flask import Flask, json

api = Flask(__name__)

@api.route('/funs', methods=['POST'])
def post_funs():
  return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run(debug=True)