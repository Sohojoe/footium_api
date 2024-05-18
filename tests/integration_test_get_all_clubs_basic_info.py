import pytest
from footium_api import GqlConnection
from footium_api.queries import get_all_clubs_basic_info
from config_integration_tests import TestWallet

@pytest.fixture
def gql_connection():
    return GqlConnection()

def test_integration_get_all_clubs_basic_info(gql_connection):
    wallet = TestWallet()
    clubs = get_all_clubs_basic_info(gql_connection, wallet.wallet_addr)

    assert isinstance(clubs, list)
    for club in clubs:
        assert 'id' in club
        assert 'name' in club
    assert clubs[0].id  == wallet.club_id
    assert clubs[0].name == wallet.club_name