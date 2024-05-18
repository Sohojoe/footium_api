import pytest
from footium_api.gql_connection import GqlConnection
from footium_api.queries import get_clubs_tournament_for_owners
import pandas as pd
from config_integration_tests import TestWallet

@pytest.fixture
def gql_connection():
    return GqlConnection()

def test_integration_get_clubs_tournament_for_owners(gql_connection):
    wallet = TestWallet()
    owner_ids = [wallet.owner_id]
    result = get_clubs_tournament_for_owners(gql_connection, owner_ids)

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert wallet.club_name in result["name"].values
    assert result.loc[wallet.club_id, "name"] == wallet.club_name
    assert result.loc[wallet.club_id, "owner_id"] == wallet.owner_id
    assert result.loc[wallet.club_id, "owner_address"].lower() == wallet.wallet_addr.lower()

    assert "name" in result.columns
    assert "division" in result.columns
    assert "position" in result.columns
    assert "league" in result.columns
    assert "tournament_name" in result.columns
    assert "tournament_type" in result.columns
    assert "owner_id" in result.columns
    assert "owner_address" in result.columns
