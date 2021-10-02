import os

def get_files_count(folder_path):
	dirListing = os.listdir(folder_path)
	return len(dirListing)
	
if __name__ == "__main__":
	print(get_files_count("."))
