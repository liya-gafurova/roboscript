import csv
import datetime
import json
import os
import time
import  xml.dom.minidom
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

roboforex_accounts_filename = 'accounts.xml'

# course_name = 'forinvestcourse' # TODO название курса , robovladelets
# secret_key = 'FysVeUnB6lOE0k9SU01lNFDGoAY8gR8GsklKsQjRzEVEGR4Rfg7T7tBjkyljQSKZxQHhpDLeb7U2y5eONrvNuEbaXFvAKK8QHj0yKRySAN193GhrqSZElpr9t7A6LEfG' # TODO get_course API key
# subscribe_period = 30 # TODO количество дней , на которое распространяется подписка
# USERNAME = 'gali4086555@gmail.com' # TODO username на get_course, админка
# PASSWORD = 'f54c045e' # TODO пароль на get_course, админка
# DATAURL = 'https://{}.getcourse.ru/user/control/surveyAnswer/list/surveyId/37241'.format(course_name) # TODO ulr до анкеты
# download_path = r'/home/lgafurova/Downloads/'  # TODO путь до Загрузок

def get_export_id(account_name:str, secret_key: str,params : str):
    str_request = 'https://{0}.getcourse.ru/pl/api/account/users?key={1}&{2}'.format(account_name, secret_key, params)
    res_json = requests.get(str_request).json()
    return res_json['info']['export_id']

def get_client_json_list(account_name : str , secret_key : str, export_id: str ):
    str_request = 'https://{0}.getcourse.ru/pl/api/account/exports/{1}?key={2}'.format(account_name, export_id, secret_key)
    return requests.get(str_request).json()

def get_orders_export_id(account_name, secret_key, status):
    str_req = 'https://{0}.getcourse.ru/pl/api/account/deals?key={1}&status={2}'.format(account_name,secret_key, status)
    json = requests.get(str_req).json()
    try:
        return json['info']['export_id']
    except Exception as e:
        print('Exception = {}'.format(e))

def get_orders_list (account_name : str , secret_key : str, export_id: str ):
    str_request = 'https://{}.getcourse.ru/pl/api/account/exports/{}?key={}'.format(account_name, export_id,secret_key)
    return requests.get(str_request).json()


def coalesce(*arg):
  for el in arg:
    if el is not None:
      return el
  return None

def find_indesies_of_fields(row: list, needed_fields:list):
    indesies =[]
    for field in needed_fields:
        if field in row:
            indesies.append(row.index(field))
    return  indesies


def get_data_from_exported_survey(file_path, needed_fields):
    # передаем файл (CSV) и список полей, которые нужно вытащить
    with open(file_path) as csvfile:
        survey_reader = csv.reader(csvfile, delimiter=';')
        iterrows = 0
        indesies = []
        accounts_all  = []
        for row in survey_reader:
            accounts = []
            if iterrows == 0:
                iterrows +=1
                indesies = find_indesies_of_fields(row, needed_fields)
            else:
                for index in indesies:
                    accounts.append(row[index])
                iterrows += 1
                accounts_all.append(accounts)
        #print('survey  = ' + str(accounts_all))
    return accounts_all

def get_json(file_name):
    with open(file_name) as orders_json:
        data = ''.join(orders_json.readlines())
    json_string= json.loads(data)
    return json_string

def get_data_from_exported_orders(json_string, needed_order_fields):
    #  передаем файл (JSON) и список полей, которые нужно вытащить
    orders_all = []

    # получаем индексы полей, где будут содержаться необходимые данные
    orders_indesies = find_indesies_of_fields(json_string['info']['fields'], needed_order_fields)

    for order in json_string['info']['items']:
        order_row = []
        # TODO сделать не списолк списков, а список кортежей
        for orders_index  in orders_indesies:
            order_row.append(order[orders_index])
        orders_all.append(order_row)
    print('orders = ' + str(orders_all))
    return  orders_all

def get_data_from_exported_accounts(accounts_filename, tag_name = 'account'):
    dom = xml.dom.minidom.parse(accounts_filename);
    xml_account_elemets = dom.getElementsByTagName(tag_name)
    print('xml = '+str([element.getAttribute('id') for element in xml_account_elemets]))
    return [element.getAttribute('id') for element in xml_account_elemets]

def filter_orders(orders : list, params:dict):
    # отфильтровать заказы по дате, статусу , продукту
    current_date = datetime.datetime.today()
    # текущая дата - длительность периода подписки
    earliest_payment_day = current_date - datetime.timedelta(days=params['subscribe_period'])
    filtered_orders = []
    for order in orders:
         # TODO убрать обращение по индексу
        order[1] =   order[1] if order[1]!= '' else default_lowest_date
        payment_date = coalesce(datetime.datetime.strptime(order[1], "%Y-%m-%d %H:%M:%S"))
        if order[3] == params['status'] and order[2] == params['Title'] and payment_date >= earliest_payment_day:
            filtered_orders.append(order)
    print('filtered_orders' + str(filtered_orders))
    return  filtered_orders

def group_survey_answers(raw_surveys: list):
    # сгруппировать по почте отвечающего на письмо. почта : список счетов
    # вернуть словарь
    keys = set([survey[0]  for survey in raw_surveys])
    survey_dict = dict.fromkeys(keys, [])
    for survey in raw_surveys:
        survey_dict[survey[0]].append(survey[1])
    print('surveys = ' + str(survey_dict))
    return  survey_dict

def get_elem_by_name(elem_list, name):
    for e in elem_list:
        if name in e.text:
            return  e


def get_csv_surveys(username , password, dataurl,course_name , driver_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(driver_path)  # , options= chrome_options
    driver.get('https://{}.getcourse.ru/cms/system/login'.format(course_name))

    # Ввод логина
    login = driver.find_element_by_name("email")
    login.clear()
    login.send_keys(username)

    # Ввод пароля
    pswd = driver.find_element_by_name("password")
    pswd.send_keys(password)

    # Жмем войти
    # 1 - ищем кнопку по названию, id формируется динамически. сначала ищем все кнопки, из них выбираем по названию
    elem = driver.find_elements_by_tag_name('button')
    el = get_elem_by_name(elem, 'Войти').click()
    time.sleep(2)  # Ждет загрузки браузера

    driver.get(dataurl)  # переходит на страницу с экспортом csv, но не экспортирует
    # экспортирует, сохраняет в загрузки
    survey_page_elem = driver.find_element_by_link_text('Экспорт (CSV)').click()
    time.sleep(5)  # ждем скачки файла


    csv_file_with_survey = group_survey_answers(get_data_from_exported_survey(file_path, needed_fields_survey))

    os.remove(file_path)

    driver.quit()
    return csv_file_with_survey

