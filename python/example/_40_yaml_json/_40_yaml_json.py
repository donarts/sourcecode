import json
import yaml # pip install pyyaml
import os

def write_file(filename, data):
	format = ''
	if filename.endswith(".json"):
		format = "json"
	if filename.endswith(".yaml"):
		format = "yaml"
	if filename.endswith(".yml"):
		format = "yml"
	with open(filename, 'w', encoding='utf-8') as fp:
		if format == 'json':
			json.dump(data, fp)
		elif format == 'yaml':
			yaml.dump(data, fp)
		else:
			fp.write(data)
		fp.close()

def write_json(filename, data):
	with open(filename, 'w', encoding='utf-8') as fp:
		json.dump(data, fp)
		fp.close()

def read_file(filename):
	format = ''
	if filename.endswith(".json"):
		format = "json"
	if filename.endswith(".yaml"):
		format = "yaml"
	if filename.endswith(".yml"):
		format = "yml"
	with open(filename, 'r', encoding='utf-8') as fp:
		if format == 'json':
			ret_data = json.load(fp)
		elif format == 'yaml':
			ret_data = yaml.load(fp,Loader=yaml.FullLoader)
		else:
			ret_data = fp.read()
		fp.close()
		return ret_data
	return None

if __name__ == "__main__":
	data = read_file("_40_yaml_data.yaml")
	print("Loaded")
	print(data)
	write_file("json_test.json",data)
	data2 = read_file("json_test.json")
	print("Loaded2")
	print(data2)
	write_file("json_test.yaml",data)
	
'''

# output

Loaded
{'json': ['rigid', 'better for data interchange'], 'yaml': ['slim and flexible', 'better for configuration'], 'object': {'key': 'value', 'array': [{'null_value': None}, {'boolean': True}, {'integer': 1}, {'alias': 'aliases are like variables'}, {'alias': 'aliases are like variables'}]}, 'paragraph': 'Blank lines denote \nparagraph breaks\n', 'content': 'Or we\ncan auto\nconvert line breaks\nto save space', 'alias': {'bar': 'baz'}, 'alias_reuse': {'bar': 'baz'}}
Loaded2
{'json': ['rigid', 'better for data interchange'], 'yaml': ['slim and flexible', 'better for configuration'], 'object': {'key': 'value', 'array': [{'null_value': None}, {'boolean': True}, {'integer': 1}, {'alias': 'aliases are like variables'}, {'alias': 'aliases are like variables'}]}, 'paragraph': 'Blank lines denote \nparagraph breaks\n', 'content': 'Or we\ncan auto\nconvert line breaks\nto save space', 'alias': {'bar': 'baz'}, 'alias_reuse': {'bar': 'baz'}}

'''