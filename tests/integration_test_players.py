from box import Box
import pandas as pd
import pytest
from footium_api.gql_connection import GqlConnection
from footium_api.queries.players import get_players_in_clubs
from config_integration_tests import TestWallet

@pytest.fixture
def gql():
    return GqlConnection()

def test_integration_get_players_in_clubs(gql):
    wallet = TestWallet()
    club_ids = [wallet.club_id]  # Assuming TestWallet provides club_id

    players_df = get_players_in_clubs(gql, club_ids)

    assert players_df is not None
    assert isinstance(players_df, pd.DataFrame)
    assert len(players_df) > 0  # Ensure there is at least one player in the dataframe

    # Access the first player using dot notation
    player_df = players_df.iloc[0]
    player = Box(player_df.to_dict())
    player.id = player_df.name  # player.id is the pandas index, so is accessed using .name

    # Check the player's main attributes
    assert isinstance(player.id, str)  # player.id is the pandas index, so is accessed using .name
    assert isinstance(player.fullName, str)
    assert isinstance(player.creationRating, int)
    assert isinstance(player.potential, int)
    assert isinstance(player.rarity, str)
    assert isinstance(player.clubId, int)
    assert isinstance(player.ownerId, (int, type(None)))  # can be None
    assert isinstance(player.originClubId, int)
    assert isinstance(player.generationId, int)
    assert isinstance(player.isAcademy, bool)
    assert isinstance(player.isReserve, bool)
    assert isinstance(player.isInitial, bool)
    assert isinstance(player.isTraining, bool)
    assert isinstance(player.isRetired, bool)
    assert isinstance(player.seed, str)
    assert isinstance(player.firstName, str)
    assert isinstance(player.lastName, str)
    assert isinstance(player.firstSeasonId, int)
    assert isinstance(player.assetId, (int, type(None)))  # assetId can be None
    assert isinstance(player.nationality, str)
    assert isinstance(player.heightMeters, float)
    assert isinstance(player.mintPrice, (float, type(None)))  # can be None
    assert isinstance(player.isPartOfAcademyMerkleTree, bool)
    assert isinstance(player.clubName, (str, type(None)))  # clubName can be None
    assert isinstance(player.clubOwnerId, (int, type(None)))  # clubOwnerId can be None

    # Check player attributes
    assert isinstance(player.age, int)
    assert isinstance(player.leadership, int)
    assert isinstance(player.condition, int)
    assert isinstance(player.stamina, int)
    assert isinstance(player.gamesSuspended, int)
    assert isinstance(player.accumulatedYellows, int)
    assert isinstance(player.isLatest, bool)
    assert isinstance(player.timestamp, int)
    assert isinstance(player.footedness, str)
    assert isinstance(player.weakFootAbility, int)
    assert isinstance(player.unlockedPotential, int)
    assert isinstance(player.usedPotential, int)
    assert isinstance(player.accumulatedMinutes, int)

    # Check positional ratings explicitly
    assert isinstance(player.CF, (float, type(None)))
    assert isinstance(player.LW, (float, type(None)))
    assert isinstance(player.RW, (float, type(None)))
    assert isinstance(player.AM, (float, type(None)))
    assert isinstance(player.LM, (float, type(None)))
    assert isinstance(player.CM, (float, type(None)))
    assert isinstance(player.RM, (float, type(None)))
    assert isinstance(player.DM, (float, type(None)))
    assert isinstance(player.LWB, (float, type(None)))
    assert isinstance(player.RWB, (float, type(None)))
    assert isinstance(player.LB, (float, type(None)))
    assert isinstance(player.CB, (float, type(None)))
    assert isinstance(player.RB, (float, type(None)))
    assert isinstance(player.GK, (float, type(None)))

    assert len(player) == 52
