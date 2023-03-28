
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

driver.get("https://www.naver.com")

driver.implicitly_wait(3)

print(driver.page_source)