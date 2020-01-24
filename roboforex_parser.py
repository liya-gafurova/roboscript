import requests
from getpass import getpass

# используя менеджер контента, можно убедиться, что ресурсы, применимые
# во время сессии будут свободны после использования
with requests.Session() as session:
    session.auth = ('gali4086555@gmail.com', 'f54c045e')

    # Instead of requests.get(), you'll use session.get()
    response = session.get('https://forinvestcourse.getcourse.ru/user/control/surveyAnswer/list/surveyId/37241')

# здесь можно изучить ответ
print(response.headers)
print(response.content)