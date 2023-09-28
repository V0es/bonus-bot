# 	При перечислении номеров или иных идентификаторов через запятую, избегайте использования пробелов.

# 	Что бы указать не все необязательные параметры, необходимо указать имя параметра, при вызове функции, например:
# 	sms.create('10000', 'текст сообщения', name='имя рассылки', test=1)

# 	результат любой функции - словарь, элементы словарей описаны на домашней странице сервиса

import logging
from typing import Dict

import requests
import json
import hashlib


class AuthAPI:

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    def __init__(self, project_name: str, api_key: str) -> None:
        self.project = project_name  # Имя проекта
        self.api_key = api_key  # API-ключ
        self.url = "http://sms.notisend.ru/api/"

    # выполнение запроса
    def do_request(self, rq_data: Dict, url: str):

        # формируем словарь
        rq_data["project"] = self.project  # 1. Добавляем в словарь POST проект
        data_list = []
        sign = ""

        for i in rq_data:  # 2. словарь POST переводим в список
            data_list.append(str(rq_data[i]))
        data_list.sort()  # 3. сортируем в алфавитном порядке

        for element in data_list:  # 4. получаем левую часть sign
            sign = sign + str(element) + ";"

        sign = sign + str(self.api_key)  # 5. получаем целый нешифрованный sign

        sign = hashlib.sha1(sign.encode("utf-8")).hexdigest()  # 6. шифруем sha1
        sign = hashlib.md5(sign.encode("utf-8")).hexdigest()  # 7. шифруем md5

        rq_data["sign"] = sign  # 8. добавляем sign в POST

        r = requests.get(self.url + url, headers=self.headers, params=rq_data)
        # print r.url
        # Когда что-то идёт не по плану, можно посмотреть GET запрос (через браузер)
        # r = requests.post(self.url+url, headers=self.headers, data=rqData)	#POST работал только с одиночными SMS

        # print(r.text)

        ansver = json.loads(r.text)
        return ansver

    # 									#
    # 			ОДИНОЧНЫЕ СМС			#
    # 									#
    def send_sms(self, recipients, message, sender="", run_at="", test=0):  # шлём SMS
        rq_data = {"recipients": recipients, "message": message, "test": test}
        if sender != "":
            rq_data["sender"] = sender

        # если указана дата-время (формат  "дд.мм.гггг чч:мм")
        # часовой пояс настраивается в личном кабинете
        if run_at != "":
            rq_data["run_at"] = run_at
        logging.info(f"Sent OTP to {recipients}")
        return self.do_request(rq_data, "message/send")

    def get_balance(self):  # узнаём баланс
        rq_data = {}
        return self.do_request(rq_data, "message/balance")

    def message_price(self, recipients, message):  # узнаём цену сообщений
        rq_data = {"recipients": recipients, "message": message, "sender": self.sender}
        return self.do_request(rq_data, "message/price")

    def phones_info(self, phones):  # узнаём информацию о номерах
        rq_data = {"phones": phones}
        return self.do_request(rq_data, "message/info")

    def sms_status(self, messages_id):  # узнаём статус SMS
        rq_data = {"messages_id": messages_id}
        return self.do_request(rq_data, "message/status")

    # 									#
    # 			РАССЫЛКИ				#
    # 									#
    def create_dist(
        self,
        include,
        message,
        exclude=0,
        sender="",
        run_at="",
        slowtime="",
        slowsize="",
        name="",
        test=0,
    ):  # Создание смс рассылки
        rq_data = {"include": include, "message": message}
        if sender != "":
            rq_data["sender"] = sender

        if slowtime != "":
            rq_data["slowtime"] = slowtime

        if slowsize != "":
            rq_data["slowsize"] = slowsize

        if name != "":
            rq_data["name"] = name

        if run_at != "":
            rq_data["run_at"] = run_at

        if exclude != 0:
            rq_data["exclude"] = exclude

        if test != 0:
            rq_data["test"] = test

        return self.do_request(rq_data, "sending/create")

    def get_groups(self, group_type):  # Запрос групп
        rq_data = {"type": group_type}
        return self.do_request(rq_data, "sending/groups")

    def dist_status(self, dist_id):  # Запрос статуса рассылки
        rq_data = {"id": dist_id}
        return self.do_request(rq_data, "sending/status")
