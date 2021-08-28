from requests.auth import HTTPBasicAuth
import requests
from pack import config
from pack.config import get_random_str, ivi_user

def test_for_reset():
    res = requests.post('http://rest.test.ivi.ru/v2/reset', auth=HTTPBasicAuth('faridazim@yandex.ru', 'APZrVp83vFNk5F'))
    assert res.status_code == 200


def test_create_new_character(case_data):
    """Тест создает персонажа, проверяет ответ"""

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
    assert res.data.get("name") == some.name
    assert res.data.get('education') == some.education
    assert res.data.get('other_aliases') == some.other_aliases

    some.name = some.name
    res = some.read()
    code = res.code

    assert code == 200
    assert res.data.get('height') == some.height
    assert res.data.get('identity') == some.identity
    assert res.data.get('universe') == some.universe
    assert res.data.get('weight') == some.weight


def test_create_already_exists_character(case_data):
    """Тест создает персонажа, который уже существует"""

    some = case_data
    some.name = ivi_user
    print(some.name)
    some.education = config.get_random_str()
    some.universe = config.get_random_str()
    some.identity = config.get_random_str()
    some.height = config.get_random_int()
    some.weight = config.get_random_int()
    some.other_aliases = config.get_random_str()
    res = some.create()
    code = res.code
    if code == 200:
        print('Specification error')
    elif code == 400:
        print(f'{ivi_user} is already exists')


def test_merge_type_fields(case_data):
    """Тест создает персонажа с измененным типом полей"""

    some = case_data
    some.name = config.get_random_int()
    some.education = config.get_random_str()
    some.universe = config.get_random_str()
    some.identity = config.get_random_str()
    some.height = config.get_random_int()
    some.weight = config.get_random_int()
    some.other_aliases = config.get_random_str()
    res = some.create()
    code = res.code
    if code == 200:
        print('Specification error')
    elif code == 400:
        print('Payload must be a valid json')



def test_character_with_empty_fields(case_data):
    """Тест создает персонажа с пустым значением"""
    some = case_data
    some.name = ''
    some.education = 'abc'
    some.universe = 'def'
    some.identity = 'fad'
    some.height = 0
    some.weight = 0
    some.other_aliases = 'ffv'
    res = some.create()
    code = res.code
    if code == 200:
        print('Specification error')
    elif code == 400:
        print("name: ['Length must be between 1 and 350.']")



def test_create_character_with_a_lot_of_content(case_data):
    '''Тест создает персонажа с большим колличеством данных'''

    url = "http://rest.test.ivi.ru/v2"
    data = open('Kratos').read()
    ints = open('ints').read()
    requests.post(url)
    some = case_data
    some.name = data
    some.education = config.get_random_str()
    some.universe = config.get_random_str()
    some.identity = config.get_random_str()
    some.height = ints
    some.weight = ints
    some.other_aliases = config.get_random_str()
    res = some.create()
    code = res.code
    if code == 200:
        print('Specification error')
    elif code == 400:
        print('Length must be between 1 and 350.')


def test_character_create_fields_not_exist(case_data):
    '''Тест создает персонажа с измененным ключем инпута'''
    some = case_data
    some.creat_not_exist()





if __name__ == "__main__":
    test_for_reset()
    test_create_new_character()
    test_create_already_exists_character()
    test_merge_type_fields()
    test_character_with_empty_fields()
    test_character_create_fields_not_exist()
    test_create_character_with_a_lot_of_content()