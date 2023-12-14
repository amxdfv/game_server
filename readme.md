
Допустимые команды для сервера:

1. Создание пользователя

{"command": "CREATE_USER", "login": "sample_text", "password": "sample_password", "name":"sample_name"}
(поле name необязательное)

Успешный ответ:

{'command': 'CREATE_USER', 'result': 'SUCCESS', 'message': 'Пользователь успешно создан'}

Неуспешный ответ:

{'command': 'CREATE_USER', 'result': 'ERROR', 'message': '(1062, "Duplicate entry \'sample_text2\' for key \'users.login\'")'}

2. Получение пользователя

{"command": "GET_USER", "login": "sample_text", "password": "sample_password"}

Успешный ответ:

{'command': 'GET_USER', 'result': 'SUCCESS', 'message': {'login': 'sample_text1', 'password': 'sample_password', 'name': None, 'date_of_creation': '2023-12-14 18:51:23', 'score': 0}}

Неуспешный ответ:

{'command': 'GET_USER', 'result': 'ERROR', 'message': 'Пользователь не найден'}
3. Обновление счета пользователя

{"command": "UPDATE_SCORE", "login": "sample_text", "password": "sample_password", "score": 100}

Успешный ответ:

{'command': 'UPDATE_SCORE', 'result': 'SUCCESS', 'message': 'Счет пользователя успешно обновлен'}

Неуспешный ответ:

{'command': 'UPDATE_SCORE', 'result': 'ERROR', 'message': 'Пользователь не найден'}