# Code-cheker

Работает для кода на python

Установка всех зависимостей:
`pip install -r requirements.txt`

Для корректного запуска модуля необходимо создать новое виртуальное окружение
с названием `venv2` 

Для проверки модуля содержится postman-коллекция `code_cheker.postman_collection.json`

В модуле реализована сеансовая аутентификация по JWT токену _(см. /auth и /login)_

### Как использовать

Нужно преобразовать проверяемый код в _base64_ строку (со всеми пробелами и табами),
затем передать её по адресу `http://yourhost:5000/chek` в .json формате

В ответе содержится вывод, информация об ошибках и время, 
за которое был выполнен код.


