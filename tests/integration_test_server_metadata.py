import pytest
from footium_api.gql_connection import GqlConnection
from footium_api.queries import get_server_timestamp  # Adjust the import path based on your project structure

@pytest.fixture
def gql():
    return GqlConnection()

def test_get_server_timestamp(gql):
    timestamp = get_server_timestamp(gql)

    assert timestamp is not None
    assert isinstance(timestamp, int)

