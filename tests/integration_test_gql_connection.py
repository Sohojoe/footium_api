import pytest
from footium_api.gql_connection import GqlConnection
from box import Box, BoxList


@pytest.fixture
def gql_connection():
    return GqlConnection()


def test_integration_send_query(gql_connection):
    query = """
query Formations {
    formations {
        id
        name
        slots {
            id
            formationId
            slotIndex
            position
            coords
        }
    }
}
    """
    response = gql_connection.send_query(query)
    
    assert isinstance(response, Box)
    assert 'formations' in response

def test_integration_send_paging_query(gql_connection):
    query = """
    query GetPlayers($take: Int, $skip: Int) {
        players(take: $take, skip: $skip) {
            id
        }
    }
    """
    variables = {}
    players_set_1 = gql_connection.send_paging_query(query, variables=variables, take=5, skip=0, stop=20)

    assert isinstance(players_set_1, BoxList)
    for player in players_set_1:
        assert 'id' in player

    players_set_2 = gql_connection.send_paging_query(query, variables=variables, take=5, skip=10, stop=1)
    assert players_set_2[0].id == players_set_1[10].id



# TODO: figure out how to test_integration_send_mutation
