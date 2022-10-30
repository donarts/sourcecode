import selenium_v1
from bs4 import BeautifulSoup


if __name__ == "__main__":
	sel = selenium_v1.selenium_v1()
	sel.create_web_driver_chrome(headless=True, download_path=".")
	# get page
	sel.get("https://www.daum.net")
	sel.driver.implicitly_wait(3)
	#print(sel.driver.page_source)

	soup = BeautifulSoup(sel.driver.page_source, "html.parser")
	result = soup.select('#wrapSearch > div.slide_favorsch > ul:nth-child(2) > li:nth-child(1) > a')
	print(f'type:{type(result)},result:{result}')
	for one in result:
		print(f'type:{type(one)},result:{one},href:{one.href},text:{one.text},get:{one.get("data-tiara-layer")}')

	result = soup.select_one('#wrapSearch > div.slide_favorsch > ul:nth-child(2) > li:nth-child(1) > a')
	print(f'type:{type(result)},result:{result}')
