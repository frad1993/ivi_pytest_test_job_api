import pytest
from requests.auth import HTTPBasicAuth
from pack import config
import requests
from pack.config import get_random_str, ivi_user

def test_for_reset():
    res = requests.post('http://rest.test.ivi.ru/v2/reset', auth=HTTPBasicAuth('faridazim@yandex.ru', 'APZrVp83vFNk5F'))
    assert res.status_code == 200

def test_delete_real_person(case_data):
    """Тест удаляет существующий обьект на сервере"""

    some = case_data
    some.name = get_random_str()
    some.education = config.get_random_str()
    some.universe = config.get_random_str()
    some.identity = config.get_random_str()
    some.height = config.get_random_int()
    some.weight = config.get_random_int()
    some.other_aliases = config.get_random_str()
    res = some.create()
    code = res.code
    print(some.name)
    assert code == 200
    url = f"http://rest.test.ivi.ru/v2/character?name={some.name}"

    payload = {}
    headers = {
        'Authorization': 'Basic ZmFyaWRhemltQHlhbmRleC5ydTpBUFpyVnA4M3ZGTms1Rg=='
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    print(response.text)



def test_delete_not_existe_person(case_data):
    some = case_data
    some.delete_not_exist()






if __name__ == "__main__":
    test_for_reset()
    test_delete_real_person()
    test_delete_not_existe_person()