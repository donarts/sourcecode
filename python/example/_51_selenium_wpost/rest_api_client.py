import requests
import selenium_v1 as selenium_v
from bs4 import BeautifulSoup

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

resp = requests.post('http://127.0.0.1:5000/stock/animal', data=data2, hooks={'response': print_roundtrip})


def get_script(url, params):
	post_script = '''
	function post_to_url(path, params, method) {
		method = method || "post";
		var form = document.createElement("form");
		form._submit_function_ = form.submit;
		form.setAttribute("method", method);
		form.setAttribute("action", path);
		for(var key in params) {
			var hiddenField = document.createElement("input");
			hiddenField.setAttribute("type", "hidden");
			hiddenField.setAttribute("name", key);
			hiddenField.setAttribute("value", params[key]);
			form.appendChild(hiddenField);
		}
		document.body.appendChild(form);
		form._submit_function_();
	}

	'''
	run_script = f'post_to_url("{url}",'
	run_script = run_script + "{"
	first = True
	for odata in params:
		if first == False:
			run_script = run_script + ","
		else:
			first = False
		run_script = run_script + odata + ':' + str(params[odata])
	run_script = run_script + "} )"
	#print(post_script + run_script)
	return post_script + run_script

sel = selenium_v.selenium_v()
sel.create_web_driver_chrome(headless=True, download_path=".")
sel.driver.execute_script(get_script("http://127.0.0.1:5000/stock/animal", data1))
print(sel.driver.page_source)

# get page
#sel.get('http://127.0.0.1:5000/stock/animal')
#sel.driver.implicitly_wait(3)

