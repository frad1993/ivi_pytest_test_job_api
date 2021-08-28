"""Модуль содержит класс для работы с типом Character"""

import json
import requests

class Character:
    """Класс персонаж"""

    def __init__(self, req):
        """Конструктор
        :param IviServerRequests req: объект позволяющий отправить запросы на сервер"""

        self.name = ""
        self.universe = ""
        self.education = ""
        self.identity = ""
        self.other_aliases = ""
        self.height = 0
        self.weight = 0
        self.__req = req
        self.__req.obj_type = 'character'

    def create(self):
        """Метод создает объект на сервере
        :return: возвращает объект содержащий ответ от сервера
        :rtype: IviServerResponse"""

        data = self.to_json()
        res = self.__req.post(data)
        return res

    def read(self):
        """Метод читает объект с сервера
        :return: возвращает объект содержащий ответ от сервера
        :rtype: IviServerResponse"""

        res = self.__req.get(self.name)
        if res.code == 200 and res.msg is None:
            self.from_json(res.data)


        return res

    def update_empty_fields(self):
        """Метод обновляет персонажа с пустым значением поля"""
        url = "http://rest.test.ivi.ru/v2/character"

        payload = json.dumps({
            "name": "uubwfu",
            "universe": "",
            "education": "High School (unfinished)",
            "weight": 104,
            "height": 1.9,
            "identity": "Publicly known"
        })
        headers = {
            'Authorization': 'Basic ZmFyaWRhemltQHlhbmRleC5ydTpBUFpyVnA4M3ZGTms1Rg==',
            'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text)



    def update(self):
        """Метод обновляет объект на сервере
        :return: возвращает объект содержащий ответ от сервера
        :rtype: IviServerResponse"""

        data = self.to_json()

        return self.__req.put(self.name, data)

    def creat_not_exist(self):
        url = "http://rest.test.ivi.ru/v2/character"

        payload = json.dumps({
            "namve": "uubwu",
            "universe": "Marvel Universe",
            "education": "High School (unfinished)",
            "weight": 104,
            "height": 1.9,
            "identity": "Publicly known"
        })
        headers = {
            'Authorization': 'Basic ZmFyaWRhemltQHlhbmRleC5ydTpBUFpyVnA4M3ZGTms1Rg==',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


    def delete(self):
        """Метод удаляет данный объект с сервера

        :return: возвращает объект содержащий ответ от сервера
        :rtype: IviServerResponse
        """
        res = self.__req.delete(self.name)
        return res

    def delete_not_exist(self):
        """Метод удалаяпт не существующего персонажа"""
        url = f"http://rest.test.ivi.ru/v2/character?name=Kratos"

        payload = {}
        headers = {
            'Authorization': 'Basic ZmFyaWRhemltQHlhbmRleC5ydTpBUFpyVnA4M3ZGTms1Rg=='
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)
        print(response.text)
    def to_json(self):
        """Метод получает JSON из данных в текущем объекте
        :return: возвращает объект содержащий ответ от сервера
        :rtype: Object"""

        return json.JSONEncoder().encode(
            {
                "education": self.education,
                "height": self.height,
                "identity": self.identity,
                "name": self.name,
                "other_aliases": self.other_aliases,
                "universe": self.universe,
                "weight": self.weight
            }
        )

    def from_json(self, data):
        """Метод заполняет текущий объект данными из JSON
        :param Object data: объект содержащий JSON данные"""

        self.education = data["education"]
        self.height = data["height"]
        self.identity = data["identity"]
        self.name = data["name"]
        self.other_aliases = data["other_aliases"]
        self.universe = data["universe"]
        self.weight = data["weight"]

    def no_correct_from_json(self, data):
        """Метод заполняет текущий объект данными из JSON
        :param Object data: объект содержащий JSON данные"""

        self.education1 = data["educationn"]
        self.height1 = data["height"]
        self.identity1 = data["identity"]
        self.name1 = data["name"]
        self.other1_aliases = data["other_aliases"]
        self.universe1 = data["universe"]
        self.weight1 = data["weight"]
