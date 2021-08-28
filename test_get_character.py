from requests.auth import HTTPBasicAuth
from pack import IviServerRequests
from pack import Character
import requests


url = 'http://rest.test.ivi.ru/v2'
iviReq = IviServerRequests.IviServerRequests(url, 'faridazim@yandex.ru', 'APZrVp83vFNk5F')
some = Character.Character(iviReq)


def test_reset():
    res = requests.post('http://rest.test.ivi.ru/v2/reset', auth=HTTPBasicAuth('faridazim@yandex.ru', 'APZrVp83vFNk5F'))
    assert res.status_code == 200


def test_get_existing_character_check_all_fields():
    """Тест получает персонажа по имени и проверяет его поля
    """

    some.name = 'Avalanche'
    res = some.read()
    code = res.code

    assert code == 200
    assert res.data.get('education') == 'Unrevealed'
    assert res.data.get('height') == 170
    assert res.data.get('identity') == 'Secret (known to the U.S. government)'
    assert res.data.get('other_aliases') == 'Jon Bloom'
    assert res.data.get('universe') == 'Marvel Universe'
    assert res.data.get('weight') == 87.75


def test_no_such_name():
    """Тест получает персонажа, которого нет на сервере и проверяет ответ"""


    some.name = 'KratosFromSparta'
    print(some.name)
    res = some.read()
    code = res.code

    if code == 400:
        print('"error": "No such name"')





def test_no_name():
    """Тест получает персонажа с пустым именем"""


    some.name = ''
    res = some.read()
    code = res.code
    if code == 400:
        print('"error": "No such name"')


if __name__ == "__main__":
    test_reset()
    test_get_existing_character_check_all_fields()
    test_no_such_name()
    test_no_name()
