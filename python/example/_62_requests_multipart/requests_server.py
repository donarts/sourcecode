from flask import Flask, json
from flask import request
api = Flask(__name__)

@api.route('/funs', methods=['POST'])
def post_funs():
    print(request.form)
    print(request.headers)
    return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run(debug=True)