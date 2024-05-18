from box import Box, BoxList
import pytest
from footium_api.gql_connection import GqlConnection
from footium_api.queries.lineups import get_lineup_for_club
from config_integration_tests import TestWallet

@pytest.fixture
def gql():
    return GqlConnection()

def test_integration_get_lineup_for_club(gql):
    wallet = TestWallet()
    club_id = wallet.club_id

    lineup = get_lineup_for_club(gql, club_id)

    assert lineup is not None
    assert isinstance(lineup, Box)

    assert isinstance(lineup.id, int)
    assert isinstance(lineup.isSelected, bool)
    assert isinstance(lineup.tacticsId, int)
    assert isinstance(lineup.clubId, int)
    assert isinstance(lineup.playerLineups, BoxList)
    assert isinstance(lineup.club, Box)
    assert isinstance(lineup.tactics, Box)
    assert len(lineup) == 7

    # playerLineups
    player_lineup = lineup.playerLineups[0]
    assert isinstance(player_lineup.id, int)
    assert isinstance(player_lineup.playerId, str)
    assert isinstance(player_lineup.lineupId, int)
    assert isinstance(player_lineup.formationSlotIndex, int)
    assert isinstance(player_lineup.isCaptain, bool)
    assert len(player_lineup) == 5

    # club.players
    assert isinstance(lineup.club.players, BoxList)
    player = lineup.club.players[0]
    assert isinstance(player.id, str)
    assert isinstance(player.firstName, str)
    assert isinstance(player.lastName, str)
    assert isinstance(player.isAcademy, bool)
    assert isinstance(player.isReserve, bool)
    assert isinstance(player.isTraining, bool)
    assert isinstance(player.isRetired, bool)
    assert isinstance(player.rarity, str)
    assert isinstance(player.playerAttributes, BoxList)
    assert isinstance(player.positionalRating, BoxList)
    assert isinstance(player.timesteppedPlayerAttributes, Box)
    assert len(player) == 11

    # club.players.playerAttributes
    player_attribute = player.playerAttributes[0]
    assert isinstance(player_attribute.id, int)
    assert isinstance(player_attribute.accumulatedYellows, int)
    assert isinstance(player_attribute.playerId, str)
    assert isinstance(player_attribute.leadership, int)
    assert isinstance(player_attribute.stamina, int)
    assert isinstance(player_attribute.timestamp, int)
    assert isinstance(player_attribute.gamesSuspended, int)
    assert isinstance(player_attribute.isLatest, bool)
    assert len(player_attribute) == 8

    # club.players.positionalRating
    positional_rating = player.positionalRating[0]
    assert isinstance(positional_rating.id, int)
    assert isinstance(positional_rating.position, str)
    assert isinstance(positional_rating.rating, float)
    assert isinstance(positional_rating.relativeCompetence, int)
    assert isinstance(positional_rating.timestamp, int)
    assert len(positional_rating) == 5

    # club.players.timesteppedPlayerAttributes
    timestepped_player_attribute = player.timesteppedPlayerAttributes
    assert isinstance(timestepped_player_attribute.condition, int)
    assert len(timestepped_player_attribute) == 1

    # tactics
    tactics = lineup.tactics
    assert isinstance(tactics.id, int)
    assert isinstance(tactics.mentality, str)
    assert isinstance(tactics.formationId, int)
    assert isinstance(tactics.formation, Box)
    assert len(tactics) == 4

    # tactics.formation
    formation = lineup.tactics.formation
    assert isinstance(formation.id, int)
    assert isinstance(formation.name, str)
    assert isinstance(formation.slots, BoxList)
    assert len(formation) == 3

    # tactics.formation.slots
    formation_slot = formation.slots[0]
    assert isinstance(formation_slot.id, int)
    assert isinstance(formation_slot.slotIndex, int)
    assert isinstance(formation_slot.position, str)
    assert isinstance(formation_slot.coords, BoxList)
    assert len(formation_slot) == 4

    assert lineup.clubId == club_id
    assert player_attribute.isLatest
    assert len(formation.slots) == 11
    assert len(lineup.playerLineups) == 17  # 11 players + 6 subs
