import csv
import json
import  xml.dom.minidom # можно конечно использовать lxml, но мб лучше избежать лишних импортов


download_path = r'/home/lgafurova/Downloads/'
export_file_name = 'export_survey_37241_10.csv'
orders_filename = '5orders.json'
roboforex_accounts_filename = 'accounts.xml'

file_path =download_path + export_file_name


needed_fields_survey = ['Email','Номер счета']
needed_fields_order = ['Номер', 'Email', 'Дата оплаты','Title',  'Статус']


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
        print ('result = ' + str(accounts_all))
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
        print('str = '+str(order))
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
    return [element.getAttribute('id') for element in xml_account_elemets]

def filter_orders():
    # отфильтровать заказы по дате, статусу , продукту
    pass


#получаем данные-анкеты
robo_getcourse_connection = get_data_from_exported_survey(file_path, needed_fields_survey)

# получаем данные - заказы
current_orders = get_data_from_exported_orders(orders_filename , needed_fields_order)

# получаем данные - счета робофорекса
roboforex_accounts = get_data_from_exported_accounts(roboforex_accounts_filename)

print('')

