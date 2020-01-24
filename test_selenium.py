import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

start_url = "https://forinvestcourse.getcourse.ru/user/control/surveyAnswer/list/surveyId/37241"
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome('./chromedriver_linux64/chromedriver',options=chrome_options)
driver.get(start_url)

cookies = driver.get_cookies()

print(driver.page_source.encode("utf-8"))
driver.quit()



