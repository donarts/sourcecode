import os
import sys

def one_open_replace_save(infile,outfile,find_str,replace_str,encoding="utf-8"):
	print(infile,"->",outfile)
	fp = open(infile, 'r', encoding=encoding)
	data = fp.read()
	fp.close()
	
	instr = str(data)
	
	instr = instr.replace(find_str,replace_str)
	
	fp = open(outfile, 'w', encoding=encoding)
	fp.write(instr)
	fp.close()

def visit_dir(dir_name, file_type, find_str, replace_str):
	for file in os.listdir(dir_name):
		if file.endswith("."+file_type):
			one_open_replace_save(os.path.join(dir_name, file),os.path.join(dir_name, file),find_str,replace_str)

def visit_dir_with_r(dir_name, file_type, find_str, replace_str):
	for root, dirs, files in os.walk(dir_name):
		for file in files:
			if file.endswith("."+file_type):
				one_open_replace_save(os.path.join(root, file),os.path.join(root, file),find_str,replace_str)


def visit_and_replace(dir_name, file_type, find_str, replace_str, rtype):
	if rtype==True:
		visit_dir_with_r(dir_name, file_type, find_str, replace_str)
	else:
		visit_dir(dir_name, file_type, find_str, replace_str)
	

if __name__ == "__main__":
	visit_and_replace("testfolder","txt","Hello","hi",True)

