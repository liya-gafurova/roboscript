import time
from lib import *
import argparse


default_lowest_date = '1900-01-01 00:00:00'
params = {'status' : 'Завершен', 'Title': 'Инвест-Клуб', 'subscribe_period' : subscribe_period }
needed_fields_survey = ['Email','Номер счета'] # TODO в зависимосмости от того, как у заказчика сформирована анкета -- вопрос к заказчику
needed_fields_order = ['Email', 'Дата оплаты','Title',  'Статус']





def createParser():
    parser = argparse.ArgumentParser()
    # создаем аргументы, которые ожидаем передавать при запуске скрипта
    parser.add_argument('--course_name', default='forinvestcourse')
    parser.add_argument('--get_course_api_key', default='FysVeUnB6lOE0k9SU01lNFDGoAY8gR8GsklKsQjRzEVEGR4Rfg7T7tBjkyljQSKZxQHhpDLeb7U2y5eONrvNuEbaXFvAKK8QHj0yKRySAN193GhrqSZElpr9t7A6LEfG')
    parser.add_argument('--subscribe_period', default=30)
    parser.add_argument('--get_course_username', default='gali4086555@gmail.com')
    parser.add_argument('--get_course_password', default='f54c045e')
    parser.add_argument('--survey_url', default='https://forinvestcourse.getcourse.ru/user/control/surveyAnswer/list/surveyId/37241')
    parser.add_argument('--downloads_path', default= r'/home/lgafurova/Downloads/')


    return  parser

if __name__ == "__main__":
    parser= createParser()
    namespase = parser.parse_args()
    LOGINURL = 'https://{}.getcourse.ru/cms/system/login'.format(namespase.course_name)
    driver_path = './chromedriver_linux64/chromedriver'
    survey_id = namespase.survey_url.split('/')[-1]
    export_file_name = 'export_survey_{}.csv'.format(survey_id)
    file_path = namespase.downloads_path + export_file_name


    # 1. Сбор данных
    # 1.1 экспорт заказов из get_course
    status = 'new'  # TODO 'payed' заказ в статусе "Завершен"
    order_export_id = get_orders_export_id(course_name, secret_key, status)
    # останавливаем скрипт для того, чтобы на сайте успели собраться данные.
    # Если второй запрос отправлять без паузы, данные не успевают собраться 'error_message': 'Файл еще не создан '
    time.sleep(10)
    orders_list_json = get_orders_list(course_name, secret_key, order_export_id)
    orders = filter_orders(get_data_from_exported_orders(orders_list_json, needed_fields_order), params=params)

    # 1.2 Сбор анкет csv
    surveys = get_csv_surveys(namespase.get_course_username, namespase.get_course_password, namespase.survey_url , namespase.course_name , driver_path)

    # 1.3 сбор данных с робофоркес
    accounts_roboforex = get_data_from_exported_accounts(
        roboforex_accounts_filename)  # TODO сделать получение из апишки

    # 2 Логика обработки
    result = {}
    for appropriate_order in orders:
        if appropriate_order[1] in surveys.keys():
            accounts = set(surveys[appropriate_order[1]])
            account_intersection = accounts.intersection(accounts_roboforex)
            result[appropriate_order[1]] = account_intersection

    print('e-mails with approved accounts = {}'.format(result))

    print('')