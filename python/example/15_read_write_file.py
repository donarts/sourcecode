import shutil
import os

def write_file(filename,str_data):
	with open(filename, 'w') as fp:
		fp.write(str_data)
		fp.close()

def read_file(filename):
	with open(filename, 'r') as fp:
		ret_data = fp.read()
		fp.close()
		return ret_data
	return None

if __name__ == "__main__":
	shutil.rmtree("temp",ignore_errors=True)
	os.makedirs("temp")

	print("make files")
	write_file("temp/a.txt","Hello")
	
	print("temp list:",os.listdir("temp"))
	print("read:")
	print(read_file("temp/a.txt"))
	
	shutil.rmtree("temp",ignore_errors=True)
	


