import pytest
from pack import IviServerRequests
from pack import Character


@pytest.fixture(scope='function')
def case_data():
    url = 'http://rest.test.ivi.ru/v2'
    iviReq = IviServerRequests.IviServerRequests(url, 'faridazim@yandex.ru', 'APZrVp83vFNk5F')
    some = Character.Character(iviReq)
    yield some