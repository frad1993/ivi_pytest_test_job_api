from requests.auth import HTTPBasicAuth
from pack import IviServerRequests
from pack import Characters
import requests


def test_0_reset():
    res = requests.post('http://rest.test.ivi.ru/v2/reset', auth=HTTPBasicAuth('faridazim@yandex.ru', 'APZrVp83vFNk5F'))
    assert res.status_code == 200
    print(res.text)


def test_1_get_all_characters():
    """Тест получает всех персонажей БД, проверяет статус код
    """

    url = 'http://rest.test.ivi.ru/v2'
    iviReq = IviServerRequests.IviServerRequests(url, 'faridazim@yandex.ru', 'APZrVp83vFNk5F')
    chars = Characters.Characters(iviReq)
    res = chars.get()
    code = res.code
    if code == 200:
        print(chars.arr)

    assert code == 200


if __name__ == "__main__":
    test_0_reset()
    test_1_get_all_characters()
