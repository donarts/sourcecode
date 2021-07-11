import os

def get_tail_byte(fname,last_bytes):
	# Open file with 'b' to specify binary mode
	with open(fname, 'rb') as file:
		file.seek(last_bytes * -1, os.SEEK_END)  # Note minus sign
		byte_data = file.read()
		return byte_data.decode('utf-8')
	return ""


if __name__ == "__main__":
	print(get_tail_byte("11_tail.py",100))
