import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

class selenium_v:
	def __init__(self):
		self.driver = None
		self.download_path = None
		return
		
	def create_web_driver_chrome(self, headless=True, download_path=None):
		options = webdriver.ChromeOptions()
		options.add_argument('disable-gpu')
		options.add_experimental_option('excludeSwitches',['enable-logging'])
		
		if headless:
			options.add_argument('headless')
		
		if download_path!=None:
			self.download_path = os.path.abspath(download_path)
			prefs = {"download.default_directory":self.download_path}
			options.add_experimental_option("prefs",prefs)
		
		if self.driver!=None:
			self.driver.close()
		self.driver = None
		
		chromedriver_autoinstaller.install()
		
		try:
			self.driver = webdriver.Chrome(options=options)
			self.driver.implicitly_wait(10)
		except Exception as e:
			print("exception",e)
		
		return self.driver
		
	def download_wait(self, timeout_min=1):
		if self.download_path==None:
			print("error can not find download path")
			return -2
		path_to_downloads = self.download_path
		seconds = 0
		dl_wait = True
		sum_after = 0
		while dl_wait and seconds < timeout_min*60:
			time.sleep(5)
			dl_wait = False
			sum_before = sum_after
			sum_after = 0
			for fname in os.listdir(path_to_downloads):
				if fname.endswith('.crdownload'):
					sum_after += os.stat(path_to_downloads+'/'+fname).st_size
					dl_wait = True
			if dl_wait and seconds > 10 and sum_before == sum_after:
				print("download timeout")
				dl_wait = False
				return -1
			seconds += 5
		return seconds
	
	def get(self,url):
		if self.driver == None:
			return -1
		return self.driver.get(url)
		
	def close(self):
		if self.driver == None:
			return -1
		return self.driver.close()
		
	def save_page_source(self, filename):
		if self.driver == None:
			return -1
		html = self.driver.page_source
		try:
			f = open(filename, 'w', encoding = 'utf-8')
			f.write(html)
			f.close()
		except:
			print("exception",e)
		return 0
		
if __name__ == "__main__":
	sel = selenium_v()
	sel.create_web_driver_chrome(headless=True,download_path=".")
	print(sel.get("https://www.daum.net"))
	print(sel.driver.page_source)
	print(sel.get("https://www.python.org/ftp/python/3.9.11/python-3.9.11-embed-amd64.zip"))
	sel.download_wait()
	print(sel.driver.page_source)
	sel.save_page_source("test.html")
