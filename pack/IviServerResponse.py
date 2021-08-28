"""Модуль содержит классы обработки ответов сервера"""

import json


class IviServerResponse:
    """Базовый класс обработки ответа от сервера"""

    def __init__(self, code, data):
        """Конструктор

        :param int code: HTTP код возврата
        :param Object data: данные полученные от сервера
        """
        self.code = code
        if self.code == 200:
            json_data = json.loads(data)
            self._result = json_data["result"]
        else:
            self._result = None
        self.msg = None
        self.data = None


class GetResponse(IviServerResponse):
    """Класс обработчик ответа на GET запрос"""

    def __init__(self, code, data):
        """Конструктор

        :param int code: HTTP код возврата
        :param Object data: данные полученные от сервера
        """
        IviServerResponse.__init__(self, code, data)

        if self.code == 200:
            if type(self._result) == str:
                self.msg = self._result
            else:
                self.data = self._result


class PostResponse(IviServerResponse):
    """Класс обработчик ответа на POST запрос"""

    def __init__(self, code, data):
        """Конструктор

        :param int code: HTTP код возврата
        :param Object data: данные полученные от сервера
        """
        IviServerResponse.__init__(self, code, data)

        if type(self._result) == str:
            self.msg = self._result
        else:
            self.data = self._result


class DeleteResponse(IviServerResponse):
    """Класс обработчик ответа на DELETE запрос"""

    def __init__(self, code, data):
        """Конструктор

        :param int code: HTTP код возврата
        :param Object data: данные полученные от сервера
        """
        IviServerResponse.__init__(self, code, data)
        if self.code == 200:
            self.data = self._result
        else:
            self.msg = 'Internal error'




class PutResponse(IviServerResponse):
    """Класс обработчик ответа на PUT запрос"""

    def __init__(self, code, data):
        """Конструктор

        :param int code: HTTP код возврата
        :param Object data: данные полученные от сервера
        """
        IviServerResponse.__init__(self, code, data)

        if self.code == 200:
            self.data = self._result

        else:
            self.msg = 'Internal error'
