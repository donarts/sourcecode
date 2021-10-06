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

data1={"cat":1,"dog":2}
data2={"cat":3,"lion":4,"bird":2}
data3={"cat":3,"dog":4}

resp = requests.get('http://127.0.0.1:5000/stock', hooks={'response': print_roundtrip})

resp = requests.get('http://127.0.0.1:5000/stock/fruit', hooks={'response': print_roundtrip})

resp = requests.get('http://127.0.0.1:5000/stock/animal', hooks={'response': print_roundtrip})

resp = requests.post('http://127.0.0.1:5000/stock/animal', json=data1, hooks={'response': print_roundtrip})

resp = requests.get('http://127.0.0.1:5000/stock', hooks={'response': print_roundtrip})

resp = requests.get('http://127.0.0.1:5000/stock/animal', hooks={'response': print_roundtrip})

resp = requests.put('http://127.0.0.1:5000/stock/animal', json=data2, hooks={'response': print_roundtrip})

resp = requests.get('http://127.0.0.1:5000/stock/animal', hooks={'response': print_roundtrip})

resp = requests.patch('http://127.0.0.1:5000/stock/animal', json=data3, hooks={'response': print_roundtrip})

resp = requests.get('http://127.0.0.1:5000/stock/animal', hooks={'response': print_roundtrip})

resp = requests.delete('http://127.0.0.1:5000/stock/animal', hooks={'response': print_roundtrip})

resp = requests.get('http://127.0.0.1:5000/stock/animal', hooks={'response': print_roundtrip})

'''
---------------- request ----------------
GET http://127.0.0.1:5000/stock
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive

None
---------------- response ----------------
200 OK http://127.0.0.1:5000/stock
Content-Type: application/json
Content-Length: 56
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT

{
  "fruit": {
    "apple": 10,
    "banana": 20
  }
}


---------------- request ----------------
GET http://127.0.0.1:5000/stock/fruit
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive

None
---------------- response ----------------
200 OK http://127.0.0.1:5000/stock/fruit
Content-Type: application/json
Content-Length: 35
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT

{
  "apple": 10,
  "banana": 20
}


---------------- request ----------------
GET http://127.0.0.1:5000/stock/animal
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive

None
---------------- response ----------------
404 NOT FOUND http://127.0.0.1:5000/stock/animal
Content-Type: application/json
Content-Length: 27
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT

{
  "error": "Not found"
}


---------------- request ----------------
POST http://127.0.0.1:5000/stock/animal
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 20
Content-Type: application/json

b'{"cat": 1, "dog": 2}'
---------------- response ----------------
201 CREATED http://127.0.0.1:5000/stock/animal
Content-Type: application/json
Content-Length: 33
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT

{
  "message": "goods created"
}


---------------- request ----------------
GET http://127.0.0.1:5000/stock
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive

None
---------------- response ----------------
200 OK http://127.0.0.1:5000/stock
Content-Type: application/json
Content-Length: 104
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT

{
  "animal": {
    "cat": 1,
    "dog": 2
  },
  "fruit": {
    "apple": 10,
    "banana": 20
  }
}


---------------- request ----------------
GET http://127.0.0.1:5000/stock/animal
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive

None
---------------- response ----------------
200 OK http://127.0.0.1:5000/stock/animal
Content-Type: application/json
Content-Length: 28
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT

{
  "cat": 1,
  "dog": 2
}


---------------- request ----------------
PUT http://127.0.0.1:5000/stock/animal
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 32
Content-Type: application/json

b'{"cat": 3, "lion": 4, "bird": 2}'
---------------- response ----------------
200 OK http://127.0.0.1:5000/stock/animal
Content-Type: application/json
Content-Length: 34
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT

{
  "message": "goods replaced"
}


---------------- request ----------------
GET http://127.0.0.1:5000/stock/animal
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive

None
---------------- response ----------------
200 OK http://127.0.0.1:5000/stock/animal
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT

{
  "bird": 2,
  "cat": 3,
  "lion": 4
}


---------------- request ----------------
PATCH http://127.0.0.1:5000/stock/animal
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 20
Content-Type: application/json

b'{"cat": 3, "dog": 4}'
---------------- response ----------------
200 OK http://127.0.0.1:5000/stock/animal
Content-Type: application/json
Content-Length: 33
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT

{
  "message": "goods updated"
}


---------------- request ----------------
GET http://127.0.0.1:5000/stock/animal
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive

None
---------------- response ----------------
200 OK http://127.0.0.1:5000/stock/animal
Content-Type: application/json
Content-Length: 56
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT

{
  "bird": 2,
  "cat": 3,
  "dog": 4,
  "lion": 4
}


---------------- request ----------------
DELETE http://127.0.0.1:5000/stock/animal
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 0

None
---------------- response ----------------
204 NO CONTENT http://127.0.0.1:5000/stock/animal
Content-Type: application/json
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT



---------------- request ----------------
GET http://127.0.0.1:5000/stock/animal
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive

None
---------------- response ----------------
404 NOT FOUND http://127.0.0.1:5000/stock/animal
Content-Type: application/json
Content-Length: 27
Server: Werkzeug/1.0.1 Python/3.8.3
Date: Wed, 06 Oct 2021 23:09:55 GMT

{
  "error": "Not found"
}
'''
