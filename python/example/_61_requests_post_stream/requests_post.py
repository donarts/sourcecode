import requests

url = 'http://127.0.0.1:5000/funs'
files = {'fl': open('test.txt', 'rb')}

r = requests.post(url, files=files)

print(vars(r))
