import pytest
from footium_api.gql_connection import GqlConnection
from footium_api.queries import get_next_fixtures
import pandas as pd
from config_integration_tests import TestWallet

@pytest.fixture
def gql_connection():
    return GqlConnection()

def test_integration_get_next_fixtures(gql_connection):
    wallet = TestWallet()
    
    club_ids = [wallet.club_id]  # Using the club ID from TestWallet
    max_games = 1
    fixtures = get_next_fixtures(gql_connection, club_ids, max_games)

    assert isinstance(fixtures, pd.DataFrame)

    # TODO: think if we want to check for more; fixtures will be empty between seasons
    # if fixtures.empty:
    #     return

    # # Check if the DataFrame contains the correct columns
    # expected_columns = [
    #     "realWorldTimestamp",
    #     "clubId",
    #     "clubName",
    #     "isHome",
    #     "tournamentName",
    #     "tournamentId",
    #     "position",
    # ]
    # for column in expected_columns:
    #     assert column in fixtures.columns

    # # Additional checks for the values in the DataFrame
    # for club_id in club_ids:
    #     assert club_id in fixtures["clubId"].values

    # # Check if the number of fixtures does not exceed max_games
    # assert len(fixtures) <= max_games

    # # Verify specific club information
    # assert wallet.club_id in fixtures["clubId"].values
    # assert wallet.club_name in fixtures["clubName"].values
