import pytest
from footium_api import GqlConnection
from footium_api.queries import get_all_clubs_basic_info

@pytest.fixture
def gql_connection():
    return GqlConnection()

def test_integration_get_all_clubs_basic_info(gql_connection):
    wallet_address = "0x0A032289552D817C15C185dBfdf43B812423Ba82"
    expected_club_id = 2879
    expected_club_name = "Rocklant"
    clubs = get_all_clubs_basic_info(gql_connection, wallet_address)

    assert isinstance(clubs, list)
    for club in clubs:
        assert 'id' in club
        assert 'name' in club
    assert clubs[0].id  == expected_club_id
    assert clubs[0].name == expected_club_name