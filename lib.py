import csv
import datetime
import json
import  xml.dom.minidom # можно конечно использовать lxml, но мб лучше избежать лишних импортов


download_path = r'/home/lgafurova/Downloads/'
export_file_name = 'export_survey_37241.csv'
orders_filename = '5orders.json'
roboforex_accounts_filename = 'accounts.xml'
subscribe_period = 30 # количество дней , на которое распространяется подписка
default_lowest_date = '1900-01-01 00:00:00'
params = {'status' : 'Завершен', 'Title': 'Инвест-Клуб', 'subscribe_period' : subscribe_period }

file_path =download_path + export_file_name


needed_fields_survey = ['Email','Номер счета']


needed_fields_order = ['Номер', 'Email', 'Дата оплаты','Title',  'Статус']

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
                print('columns = '+ str(row))
                iterrows +=1
                indesies = find_indesies_of_fields(row, needed_fields)
                print('')
            else:
                print('rows = ' + str(row))
                for index in indesies:
                    accounts.append(row[index])
                iterrows += 1
                accounts_all.append(accounts)
        print('survey  = ' + str(accounts_all))
    return accounts_all


def get_data_from_exported_orders(file_name, needed_order_fields):
    #  передаем файл (JSON) и список полей, которые нужно вытащить
    orders_all = []
    with open(file_name) as orders_json:
        data = ''.join(orders_json.readlines())
    json_string= json.loads(data)

    # получаем индексы полей, где будут содержаться необходимые данные
    orders_indesies = find_indesies_of_fields(json_string['info']['fields'], needed_order_fields)

    for order in json_string['info']['items']:
        # print('str = '+str(order))
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
        order[2] =   order[2] if order[2]!= '' else default_lowest_date
        payment_date = coalesce(datetime.datetime.strptime(order[2], "%Y-%m-%d %H:%M:%S"))
        if order[4] == params['status'] and order[3] == params['Title'] and payment_date >= earliest_payment_day:
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
    print(survey_dict)
    return  survey_dict



#получаем данные-анкеты
surveys = group_survey_answers(get_data_from_exported_survey(file_path, needed_fields_survey))
# получаем данные - заказы
orders = filter_orders(get_data_from_exported_orders(orders_filename , needed_fields_order), params = params)

# получаем данные - счета робофорекса
accounts_roboforex = get_data_from_exported_accounts(roboforex_accounts_filename)

result = {}
for appropriate_order in orders:
    if appropriate_order[1] in surveys.keys():
        accounts = set(surveys[appropriate_order[1]])
        account_intersection = accounts.intersection(accounts_roboforex)
        result[appropriate_order[1]] = account_intersection

print('RESULT = {}'.format(result))

