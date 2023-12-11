# Скрипты для просмотра и отправки сообщений в чат

## Просмотр сообщений чата
Использование скрипта для просмотра сообщений в чате:

```
usage: read_messages.py [-h] [-host HOST] [-port PORT] [-logfile LOGFILE]

Утилита для чтения сообщений чата

optional arguments:
  -h, --help        show this help message and exit
  -host HOST        Имя хоста (default=minechat.dvmn.org)
  -port PORT        Номер порта (default=5000)
  -logfile LOGFILE  Имя файла логов (default=logfile.txt)
```

## Использование скрипта для регистрации и отправки сообщений

```
usage: send_messages.py [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-hs HOST] [-p PORT] [-t TOKEN] [-r {False,True}]
                        [-n NAME]
                        message

Утилита для отправки сообщений в чат

positional arguments:
  message               Отправляемое в чат сообщение, обязательный параметр

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Уровень логирования (по умолчанию: INFO)
  -hs HOST, --host HOST
                        Имя хоста (default=minechat.dvmn.org)
  -p PORT, --port PORT  Номер порта (default=5050)
  -t TOKEN, --token TOKEN
                        Токен для подключения к чату, по умолчанию берется из файла .env
  -r {False,True}, --reg {False,True}
                        Нужна регистрация? (default=False)
  -n NAME, --name NAME  Имя пользователя при регистрации (default=User)
```
## Пример отправки сообщения с регистрацией нового пользователя:
```
python3 send_messages.py Привет -r True
2023-12-11 18:57:29,358 - register - Open the connection
2023-12-11 18:57:29,388 - register - sender: Hello %username%! Enter your personal hash or leave it empty to create new account.
2023-12-11 18:57:29,415 - register - sender: Enter preferred nickname below:
2023-12-11 18:57:29,455 - register - sender: {"nickname": "Condescending User", "account_hash": "########-####-####-####-############"}
2023-12-11 18:57:29,456 - register - Токен: ########-####-####-####-############ - сохранен в файл .env
2023-12-11 18:57:29,457 - submit_message - Сообщение: "Привет" - отправлено
2023-12-11 18:57:29,457 - work_connection - Close the connection
```

## Как установить
Python3 должен быть установлен. Затем используйте `pip`  для установки зависимостей:
```
pip install -r requirements.txt
```
Рекомендуется использовать [virtualenv/venv](https://virtualenv.pypa.io/en/latest/index.html) для изоляции проекта.


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org/).
 
