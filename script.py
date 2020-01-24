import requests
import time

# документация к getcourse API
# https://getcourse.ru/blog/275796?gcmes=3912939093&gcmlg=31873
# https://getcourse.ru/blog/275993
# https://getcourse.ru/blog?tagNames=%D1%8D%D0%BA%D1%81%D0%BF%D0%BE%D1%80%D1%82&archived=actual
# https://getcourse.ru/help/api#users

# сгенерировать секретный ключ https://forinvestcourse.getcourse.ru/saas/account/api
# get запрос на эспорт клиентов
# get запрос на получение данных о клиентах
course_name = 'forinvestcourse'
secret_key = 'FysVeUnB6lOE0k9SU01lNFDGoAY8gR8GsklKsQjRzEVEGR4Rfg7T7tBjkyljQSKZxQHhpDLeb7U2y5eONrvNuEbaXFvAKK8QHj0yKRySAN193GhrqSZElpr9t7A6LEfG'



def get_export_id(account_name:str, secret_key: str,params : str):
    str_request = 'https://{0}.getcourse.ru/pl/api/account/users?key={1}&{2}'.format(account_name, secret_key, params)
    res_json = requests.get(str_request).json()
    print('export_id = {}'.format(res_json['info']['export_id']))
    return res_json['info']['export_id']

def get_client_json_list(account_name : str , secret_key : str, export_id: str ):
    str_request = 'https://{0}.getcourse.ru/pl/api/account/exports/{1}?key={2}'.format(account_name, export_id, secret_key)
    return requests.get(str_request).json()

def get_orders_export_id(account_name, secret_key, params):
    str_req = 'https://{0}.getcourse.ru/pl/api/account/deals?key={1}&status={2}'.format(account_name,secret_key, 'new')
    json = requests.get(str_req).json()
    print('order_export_id = '+str(json['info']['export_id']))
    return  json['info']['export_id']

def get_orders_list (account_name : str , secret_key : str, export_id: str ):
    str_request = 'https://{}.getcourse.ru/pl/api/account/exports/{}?key={}'.format(account_name, export_id,secret_key)
    print(requests.get(str_request).json())
    return requests.get(str_request).json()

# TODO опредилить статус пользователя, имеющего оплаченную подписку
export_id = get_export_id(course_name, secret_key, 'status=active' )
# останавливаем скрипт для того, чтобы на сайте успели собраться данные.
# Если второй запрос отправлять без паузы, данные не успевают собраться 'error_message': 'Файл еще не создан '
time.sleep(10)

exported_clients = get_client_json_list(course_name, secret_key,export_id)
print(exported_clients)

# экспорт заказов
status = 'payed'
params = {'status':status}
order_export_id = get_orders_export_id(course_name, secret_key, params)
time.sleep(10)
get_orders_list(course_name, secret_key,order_export_id)