from requests import get
from os.path import exists
import zipfile


def download(url, file_name=None):
	if not file_name:
		file_name = url.split('/')[-1]

	with open(file_name, "wb") as file:
		response = get(url)
		file.write(response.content)


if __name__ == '__main__':
	zip_folder = r"cats_and_dogs_filtered"
	url = "https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip"

	if not exists(zip_folder+".zip"):
		print("download data")
		download(url)

	if not exists(zip_folder):
		print("unzip")
		zip_ref = zipfile.ZipFile(zip_folder+".zip", 'r')
		zip_ref.extractall()
		zip_ref.close()
