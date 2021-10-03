import requests

def print_roundtrip(response, *args, **kwargs):
	format_headers = lambda d: '\n'.join(f'{k}: {v}' for k, v in d.items())
	print((""
		"---------------- request ----------------\n"
		"{req.method} {req.url}\n"
		"{reqhdrs}\n"
		"\n"
		"{req.body}\n"
		"---------------- response ----------------\n"
		"{res.status_code} {res.reason} {res.url}\n"
		"{reshdrs}\n"
		"\n"
		"{res.text}\n"
		"").format(
		req=response.request, 
		res=response, 
		reqhdrs=format_headers(response.request.headers), 
		reshdrs=format_headers(response.headers), 
	))

params = {'param1':'v1','param2':2}
params['param0']=1
print("requests.get('http://127.0.0.1:5000/funs', params=params")
resp = requests.get('http://127.0.0.1:5000/funs', params=params, hooks={'response': print_roundtrip})
print("**************")
params['param0']=2
print("requests.get('http://127.0.0.1:5000/funs', data=params")
resp = requests.get('http://127.0.0.1:5000/funs', data=params, hooks={'response': print_roundtrip})
print("**************")
params['param0']=3
print("requests.post('http://127.0.0.1:5000/funs', params=params")
resp = requests.post('http://127.0.0.1:5000/funs', params=params, hooks={'response': print_roundtrip})
print("**************")
params['param0']=4
print("requests.post('http://127.0.0.1:5000/funs', data=params")
resp = requests.post('http://127.0.0.1:5000/funs', data=params, hooks={'response': print_roundtrip})
print("**************")
params['param0']=5
print("requests.post('http://127.0.0.1:5000/funs', json=params")
resp = requests.post('http://127.0.0.1:5000/funs', json=params, hooks={'response': print_roundtrip})
print("**************")
