from box import Box, BoxList
import pytest
from footium_api.gql_connection import GqlConnection
from footium_api.queries.formations import get_formations_as_pd, get_formations
import pandas as pd

expected_positions = ["CF", "LW", "RW", "AM", "LM", "CM", "RM", "DM", "LWB", "RWB", "LB", "CB", "RB", "GK"]
expected_formations = [
    '3-4-3', '3-4-3-A', '3-5-2', '3-1-4-2', '3-4-1-2', '5-3-2', 
    '5-4-1', '5-4-1-D', '5-2-1-2', '5-2-3', '4-4-2', '4-4-2-H', 
    '4-1-2-1-2-N', '4-1-2-1-2', '4-5-1', '4-2-3-1', '4-3-3', 
    '4-3-3-A', '4-3-3-D', '4-3-3-H', '4-1-4-1', '4-2-2-2', '4-3-1-2'
    ]

@pytest.fixture
def gql():
    return GqlConnection()

def test_get_formations_as_pd(gql):
    formations = get_formations_as_pd(gql)

    assert isinstance(formations, pd.DataFrame)
    assert not formations.empty
    assert len(formations) == len(expected_formations)

    # Check if the DataFrame contains the correct index and columns
    assert all(col in formations.columns for col in expected_positions)

    # Check if the DataFrame contains the correct formations
    assert all(form in formations.index for form in expected_formations)

    # Check that each row sums to 11 players
    for idx, row in formations.iterrows():
        assert row.sum() == 11, f"Total positions for formation {idx} do not sum to 11"

def test_get_formations(gql):
    formations = get_formations(gql)
    assert isinstance(formations, BoxList)
    assert len(formations) > 0
    assert all("name" in form for form in formations)
    # enumerate expected_formations
    for f in expected_formations:
        assert any(f == form["name"] for form in formations)
    assert len(formations) == len(expected_formations)
    
    for formation in formations:
        assert isinstance(formation.id, int)
        assert isinstance(formation.name, str)
        assert isinstance(formation.slots, BoxList)
        assert len(formation.slots) == 11

        for slot in formation.slots:
            assert isinstance(slot.id, int)
            assert isinstance(slot.formationId, int)
            assert isinstance(slot.slotIndex, int)
            assert isinstance(slot.position, str)
            assert isinstance(slot.coords, BoxList)

            assert slot.position in expected_positions


    