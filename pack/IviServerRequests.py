"""Модуль содержит класс обработки ответов сервера"""

import requests
from requests.auth import HTTPBasicAuth
from pack.IviServerResponse import *
import urllib.parse


class IviServerRequests:
    """Класс отправки запросов на тестовый сервер ivi"""

    def __init__(self, url, login, password):
        """Конструктор

        :param str url: URL сервера с протоколом например http://some.ru
        :param str login: логин для аутентификации на сервере
        :param str password: пароль для аутентификации на сервере
        """
        self._url = url
        self._login = login
        self._password = password
        self._headers = {'content-type': 'application/json'}
        self._auth = HTTPBasicAuth(login, password)

    def get(self, name=None):
        """Метод отправки GET запроса

        :param str name: имя CRUD объекта
        :return: результат отправки запроса на сервер
        :rtype: IviServerResponse
        """
        #url = self._url + '/' + self.obj_type
        url = '{}{}{}'.format(self._url, urllib.parse.quote('/'), self.obj_type)
        params = {}
        if name:
            params['name'] = name
        response = requests.get(url, params=params, auth=self._auth, headers=self._headers)
        return GetResponse(response.status_code, response.text)

    def post(self, data):
        """Метод отправки POST запроса

        :param JSON data: данные для обновления на  сервере
        :return: результат отправки запроса на сервер
        :rtype: IviServerResponse
        """
        #url = self._url + '/' + self.obj_type
        url = '{}{}{}'.format(self._url, urllib.parse.quote('/'), self.obj_type)
        response = requests.post(url, auth=self._auth, data=data, headers=self._headers)
        #
        return PostResponse(response.status_code, response.text)

    def put(self, name, data):
        """Метод отправки PUT запроса

        :param str name: имя CRUD объекта
        :param JSON data: данные для обновления на  сервере
        :return: результат отправки запроса на сервер
        :rtype: IviServerResponse
        """
        #url = self._url + '/' + self.obj_type + '/' + name
        url = '{}{}{}'.format(self._url, urllib.parse.quote('/'), self.obj_type)
        response = requests.put(url, auth=self._auth, data=data, headers=self._headers)
        return PutResponse(response.status_code, response.text)

    def delete(self, data):
        """Метод отправки DELETE запроса

        :param str name: имя CRUD объекта
        :return: результат отправки запроса на сервер
        :rtype: IviServerResponse
        """
        #url = self._url + '/' + self.obj_type + '/' + name
        url = '{}{}{}'.format(self._url, urllib.parse.quote('/'), self.obj_type)
        response = requests.delete(url, auth=self._auth, data=data, headers=self._headers)

        return DeleteResponse(response.status_code, response.text)
        # тут можно обработать идентификатор удаленного объекта
        # if "is deleted" in res.msg:
        #     res.msg = None


