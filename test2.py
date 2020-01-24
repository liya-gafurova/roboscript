import os
import  time
import requests
from selenium import webdriver
from requests.auth import HTTPBasicAuth
from selenium.webdriver.chrome.options import Options

def get_elem_by_name(elem_list, name):
    for e in elem_list:
        if name in e.text:
            return  e

USERNAME = 'gali4086555@gmail.com' # put correct usename here
PASSWORD = 'f54c045e' # put correct password here
driver_path = './chromedriver_linux64/chromedriver'
LOGINURL = 'https://forinvestcourse.getcourse.ru/cms/system/login'
# нужно либо передавать id анкеты, либо как по имени искать
DATAURL = 'https://forinvestcourse.getcourse.ru/user/control/surveyAnswer/list/surveyId/37241'
download_path = r'/home/lgafurova/Downloads/'
export_file_name = 'export_survey_37241.csv'
chrome_options = Options()
chrome_options.add_argument("--headless")



driver = webdriver.Chrome(driver_path) #, options= chrome_options
driver.get(LOGINURL)

# Ввод логина
login = driver.find_element_by_name("email")
login.clear()
login.send_keys(USERNAME)

# Ввод пароля
pswd = driver.find_element_by_name("password")
pswd.send_keys(PASSWORD)

# Жмем войти
# 1 - ищем кнопку по названию, id формируется динамически. сначала ищем все кнопки, из них выбираем по названию
elem = driver.find_elements_by_tag_name('button')
el = get_elem_by_name(elem, 'Войти').click()
time.sleep(2) # Ждет загрузки браузера

print('Новая страница: ', driver.current_url)

driver.get(DATAURL) # переходит на страницу с экспортом csv, но не экспортирует
# экспортирует, сохраняет в загрузки
survey_page_elem = driver.find_element_by_link_text('Экспорт (CSV)').click()
time.sleep(5) # ждем скачки файла
print('')

path = download_path+export_file_name
with open(path) as file:
    for line in file:
        print(line)

#os.remove(path)

driver.quit()