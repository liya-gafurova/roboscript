import  time
import requests
from selenium import webdriver
from requests.auth import HTTPBasicAuth
from selenium.webdriver.chrome.options import Options

USERNAME = 'gali4086555@gmail.com' # put correct usename here
PASSWORD = 'f54c045e' # put correct password here
driver_path = './chromedriver_linux64/chromedriver'


LOGINURL = 'https://forinvestcourse.getcourse.ru/cms/system/login?required=true'
DATAURL = 'https://forinvestcourse.getcourse.ru/user/control/surveyAnswer/list/surveyId/37241'

chrome_options = Options()
#chrome_options.add_argument("--headless")

session = requests.Session()
www_request = session.get(LOGINURL, auth=HTTPBasicAuth(USERNAME, PASSWORD), allow_redirects=True)

driver = webdriver.Chrome(driver_path,options=chrome_options)
# chrome needed to open the page before add the cookies
driver.get(LOGINURL)

cookies = session.cookies.get_dict()
for key in cookies:
    driver.add_cookie({'name': key, 'value': cookies[key]})
    print(str(key) + '  '+str(cookies[key]))

time.sleep(10)
print('After cookies')
driver.get(LOGINURL)


