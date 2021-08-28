"""Модуль содержит класс для получения списка объектов типа Character с сервера"""


class Characters:
    """Класс персонажи"""

    def __init__(self, req):
        """Конструктор

        :param IviServerRequests req: объект позволяющий отправить запросы на сервер
        """
        self.arr = []
        self.__req = req
        self.__req.obj_type = 'characters'

    def get(self):
        """Метод получает список объектов с сервера

        :return: возвращает масив объектов типа Character с сервера
        :rtype: Character[]
        """
        res = self.__req.get()
        if res.code == 200:
            self.arr = res.data
        return res
