import shutil
import os

def write_file(filename,str_data):
	with open(filename, 'w') as fp:
		fp.write(str_data)
		fp.close()

def remove_oldest_file(folder,rcount=-1):
	if len(os.listdir(folder))==0:
		return None
	ret = []
	if rcount==-1:
		oldest_file = (sorted([folder+"/"+f for f in os.listdir(folder)], key=os.path.getctime))[0]
		os.remove(oldest_file)
		ret.append(oldest_file)
	else:
		while len(os.listdir(folder))>rcount:
			oldest_file = (sorted([folder+"/"+f for f in os.listdir(folder)], key=os.path.getctime))[0]
			os.remove(oldest_file)
			ret.append(oldest_file)
			
	return ret

if __name__ == "__main__":
	shutil.rmtree("temp",ignore_errors=True)
	os.makedirs("temp")

	write_file("temp/100.txt","*300")
	write_file("temp/200.txt","*200")
	write_file("temp/300.txt","*100")
	
	print("temp list:",os.listdir("temp"))
	print("removed:",remove_oldest_file("temp"))
	print("temp list:",os.listdir("temp"))
	
	write_file("temp/400.txt","*400")
	write_file("temp/500.txt","*500")
	
	print("temp list:",os.listdir("temp"))
	print("removed:",remove_oldest_file("temp",2))
	print("temp list:",os.listdir("temp"))
	
	shutil.rmtree("temp",ignore_errors=True)
	
