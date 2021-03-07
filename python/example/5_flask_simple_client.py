import requests

resp = requests.get('http://127.0.0.1:5000/funs')
print(resp.status_code)
print(resp.text)

task = {"summary": "test", "description": "test" }
resp = requests.post('http://127.0.0.1:5000/funs', json=task)
print(resp.status_code)
print(resp.text)
