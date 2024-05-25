import pytest
from unittest.mock import patch, MagicMock
from footium_api import GqlConnection, CachedGqlConnection
from gql.transport.exceptions import TransportQueryError
from box import Box, BoxList


@pytest.fixture
def gql_connection():
    with patch('footium_api.gql_connection.Client') as MockClient:
        yield GqlConnection()
        MockClient.reset_mock()

@pytest.fixture
def cached_gql_connection(gql_connection):
    return CachedGqlConnection(gql_connection, ttl=300, cache_dir='./test_cache')


def test_send_query_success(cached_gql_connection):
    mock_response = {'data': {'some_query': 'some_data'}}
    cached_gql_connection.client.execute = MagicMock(return_value=mock_response)
    
    query = """
    query {
        some_query
    }
    """
    response = cached_gql_connection.send_query(query)
    
    assert isinstance(response, Box)
    assert response.data.some_query == 'some_data'
    cached_gql_connection.client.execute.assert_called_once()


def test_send_query_with_variables(cached_gql_connection):
    mock_response = {'data': {'some_query': 'some_data'}}
    cached_gql_connection.client.execute = MagicMock(return_value=mock_response)
    
    query = """
    query($var: String) {
        some_query(var: $var)
    }
    """
    variables = {"var": "test_value"}
    response = cached_gql_connection.send_query(query, variables=variables)
    
    assert isinstance(response, Box)
    assert response.data.some_query == 'some_data'
    cached_gql_connection.client.execute.assert_called_once_with(
        cached_gql_connection.client.execute.call_args[0][0],
        variable_values=variables,
        operation_name=None
    )


def test_send_paging_query(cached_gql_connection):
    # Mock response for the first page
    mock_response_page1 = {'some_query': ['data1', 'data2']}
    # Mock response for the second page, which ends the pagination
    mock_response_page2 = {'some_query': []}
    
    cached_gql_connection.client.execute = MagicMock(side_effect=[mock_response_page1, mock_response_page2])

    query = """
    query($skip: Int, $take: Int) {
        some_query(skip: $skip, take: $take)
    }
    """
    response = cached_gql_connection.send_paging_query(query, page_size=2)

    # Check that the response is a list wrapped in a BoxList
    assert isinstance(response, BoxList)
    assert len(response) == 2
    assert response[0] == 'data1'
    assert response[1] == 'data2'
    assert cached_gql_connection.client.execute.call_count == 2  # Ensure the execute method was called twice



def test_send_mutation_success(cached_gql_connection):
    mock_response = {'submitAction': {'result': 'success'}}
    cached_gql_connection.client.execute = MagicMock(return_value=mock_response)
    
    query = """
    mutation {
        submitAction {
            result
        }
    }
    """
    response = cached_gql_connection.send_mutation(query)
    
    assert isinstance(response, Box)
    assert response.result == 'success'
    cached_gql_connection.client.execute.assert_called_once()


def test_send_mutation_failure(cached_gql_connection):
    cached_gql_connection.client.execute = MagicMock(side_effect=TransportQueryError('Error message'))
    
    query = """
    mutation {
        submitAction {
            result
        }
    }
    """
    response = cached_gql_connection.send_mutation(query)
    
    assert isinstance(response, Box)
    assert response.code == '500'
    assert response.error == 'Internal Server Error'
    assert response.message == 'Error message'
    cached_gql_connection.client.execute.assert_called_once()
