from requests.auth import HTTPBasicAuth
import requests
from pack.config import ivi_user, get_random_str, get_random_int


def test_reset():
    res = requests.post('http://rest.test.ivi.ru/v2/reset', auth=HTTPBasicAuth('faridazim@yandex.ru', 'APZrVp83vFNk5F'))
    assert res.status_code == 200


def test_update_existing_character(case_data):
    """Тест обновляет существующего персонажа на сервере"""

    some = case_data
    some.name = get_random_str()
    some.education = 'High'
    some.universe = 'DC'
    some.identity = 'Publicly'
    some.height = 22
    some.weight = 123
    some.other_aliases = "Trand"
    res = some.create()
    code = res.code
    assert code == 200

    some.name = some.name
    some.education = 'High School21'
    some.universe = 'Marvel2'
    some.identity = 'Publicly2'
    some.height = 155
    some.weight = 105
    some.other_aliases = 'True'
    res = some.update()
    code2 = res.code

    assert code2 == 200
    assert res.data.get('education') == 'High School21'
    assert res.data.get('height') == 155
    assert res.data.get('weight') == 105
    assert res.data.get('identity') == 'Publicly2'
    assert res.data.get('other_aliases') == 'True'
    assert res.data.get('universe') == 'Marvel2'


def test_update_not_exist_character(case_data):
    """Тест обновляет несуществующего персонажа на сервере
    """

    some = case_data
    some.name = ivi_user + str(1)
    some.education = 'High School'
    some.universe = 'Marvel'
    some.identity = 'Publicly'
    some.height = 150
    some.weight = 100
    some.other_aliases = 'None'
    res = some.update()
    code = res.code
    if code == 200:
        print('Specification error')
    elif code == 400:
        print("No such name")



def test_merge_type_fields(case_data):
    """Тест обновляет персонажа с измененными типами полей"""

    some = case_data
    some.name = 'Avalanche'
    some.education = 234
    some.universe = 433
    some.identity = 324
    some.height = 'small'
    some.weight = 'to fat'
    some.other_aliases = 2
    res = some.update()
    code = res.code

    if code == 200:
        print('Specification error')
    elif code == 400:
        print('"error": "name: ["Missing data for required field."]"')




def test_empty_fields(case_data):
    """Тест обновляет персонажа с пустыми полями"""

    some = case_data
    some.update_empty_fields()




if __name__ == "__main__":
    test_reset()
    test_update_existing_character()
    test_update_not_exist_character()
    test_merge_type_fields()
    test_empty_fields()

