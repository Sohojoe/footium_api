from box import Box
import pytest
from footium_api.gql_connection import GqlConnection
from footium_api.queries import get_clubs_tournament_for_owners, get_clubs_tournament_for_wallet
import pandas as pd
from config_integration_tests import TestWallet

@pytest.fixture
def gql_connection():
    return GqlConnection()

def test_get_clubs_tournament_for_owners(gql_connection):
    wallet = TestWallet()
    owner_ids = [wallet.owner_id]
    result = get_clubs_tournament_for_owners(gql_connection, owner_ids)

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert wallet.club_name in result["name"].values
    assert result.loc[wallet.club_id, "name"] == wallet.club_name
    assert result.loc[wallet.club_id, "owner_id"] == wallet.owner_id
    assert result.loc[wallet.club_id, "owner_address"].lower() == wallet.wallet_addr.lower()

def test_get_clubs_tournament_for_wallet(gql_connection):
    wallet = TestWallet()
    wallet_addr = wallet.wallet_addr
    result = get_clubs_tournament_for_wallet(gql_connection, wallet_addr)

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert wallet.club_name in result["name"].values
    assert result.loc[wallet.club_id, "name"] == wallet.club_name
    assert result.loc[wallet.club_id, "owner_id"] == wallet.owner_id
    assert result.loc[wallet.club_id, "owner_address"].lower() == wallet.wallet_addr.lower()

def test_clubs_tournament_fields(gql_connection):
    wallet = TestWallet()
    owner_ids = [wallet.owner_id]
    result = get_clubs_tournament_for_owners(gql_connection, owner_ids)

    # Access the first club using dot notation
    club_df = result.iloc[0]
    club = Box(club_df.to_dict())
    club.id = int(club_df.name)  # club.id is the pandas index, so it is accessed using .name

    # Check the club's main attributes
    assert isinstance(club.id, int) 
    assert isinstance(club.name, str)
    assert isinstance(club.division, int)
    assert isinstance(club.position, int)
    assert isinstance(club.league, int)
    assert isinstance(club.tournament_name, str)
    assert isinstance(club.tournament_type, str)
    assert isinstance(club.owner_id, int)
    assert isinstance(club.owner_address, str)
