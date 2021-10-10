import requests
from bs4 import BeautifulSoup
import re

def find_questions(bs_data):
	bsret = bs_data.find_all("div",attrs={"class":"flex--item"})
	for bsone in bsret:
		if ("questions" in bsone.text) and not ("fc-medium" in bsone.get("class")):
			return int(bsone.text.strip().split(" ")[0].strip())

def bs_example(data):
	ret = {}
	soup = BeautifulSoup(data,"html.parser")
	sresult = soup.find_all("div",attrs={"class":"s-card js-tag-cell d-flex fd-column"})
	for rone in sresult:
		#print(rone)
		#print(rone.find("a",attrs={"class":"post-tag"}).text)
		#print(find_questions(rone))
		#print(int(rone.find("a",href=re.compile(r"days=1")).text.strip().split(" ")[0].strip()))
		#print(int(rone.find("a",href=re.compile(r"days=7")).text.strip().split(" ")[0].strip()))
		#print("##########################")
		tag = rone.find("a",attrs={"class":"post-tag"}).text
		ret[tag] = [find_questions(rone),int(rone.find("a",href=re.compile(r"days=1")).text.strip().split(" ")[0].strip()),int(rone.find("a",href=re.compile(r"days=7")).text.strip().split(" ")[0].strip())]
	return ret

def write_file(filename,str_data):
	with open(filename, 'w', encoding='utf-8') as fp:
		fp.write(str_data)
		fp.close()
		
def f1(x):
	return x[1][1]
def f2(x):
	return x[1][2]

def print_dict(dict_data):
	for key,data in dict_data:
		print(key,data)

if __name__ == "__main__":
	USE_FILE = False
	if USE_FILE:
		ret = bs_example(open("test.html",encoding='utf-8'))
	else:
		resp = requests.get('https://stackoverflow.com/tags')
		write_file("test.html",resp.text)
		ret = bs_example(resp.text)
		
	print(ret)
	print("------------------ sorted days=1")
	data_ = sorted(ret.items(),key=f1,reverse=True)
	print_dict(data_)
	print("------------------ sorted days=7")
	data_ = sorted(ret.items(),key=f2,reverse=True)
	print_dict(data_)
