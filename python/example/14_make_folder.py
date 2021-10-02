import os
import shutil

def makefolder(folder_name):
	if folder_name!='' and not os.path.exists(folder_name):
		os.makedirs(folder_name)

if __name__ == "__main__":
	shutil.rmtree("temp",ignore_errors=True)	
	makefolder("temp/temp")
	print("current list:",os.listdir("."))
	print("temp list:",os.listdir("temp"))
	print("temp/temp list:",os.listdir("temp/temp"))
	shutil.rmtree("temp",ignore_errors=True)


