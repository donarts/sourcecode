import os

def get_tail_line(fname,lines):
	fsize = os.stat(fname).st_size
	bufsize = fsize/1024+1
	iter = 0
	if lines == 0:
		return ''
	with open(fname) as f:
		if bufsize > fsize:
			bufsize = fsize-1
		while True:
			iter +=1
			f.seek(fsize-bufsize*iter)
			data = []
			data.extend(f.readlines())
			if len(data) > lines or f.tell() == 0:
				#print(data)
				return (''.join(data[-(lines):]))

if __name__ == "__main__":
	print(get_tail_line("11_tail_line.py",6))