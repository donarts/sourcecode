import requests

url = 'http://127.0.0.1:5000/funs'
data = {"key1": "value1", "key2": "value2"}

r = requests.post(url, data=data)
print(r.request.headers)
print(r.request.body)

files1 = {'fl': open('test.txt', 'rb')}
r = requests.post(url, files=files1)
print(r.request.headers)
print(r.request.body)

files2 = {'fl': open('test.txt', 'rb')}
r = requests.post(url, data=data, files=files2)
print(r.request.headers)
print(r.request.body)

files_dummy = {'fl': None}
r = requests.post(url, data=data, files=files_dummy)
print(r.request.headers)
print(r.request.body)