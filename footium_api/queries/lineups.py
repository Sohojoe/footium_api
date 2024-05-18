from footium_api import GqlConnection


def get_lineup_for_club(gql: GqlConnection, club_id: int, is_academy: bool):
    query = """
query Tactics_Query($clubId: Int, $isAcademy: Boolean) {
  # ...TacticsPageLayout_Fragment
  lineups(where: {clubId: {equals: $clubId}, isSelected: {equals: true}}) {
    id
    isSelected
    tacticsId
    clubId
    playerLineups {
      id
      playerId
      lineupId
      formationSlotIndex
      isCaptain
      __typename
    }
    club {
      players(where: {isAcademy: {equals: $isAcademy}}) {
        id
        firstName
        lastName
        isAcademy
        isReserve
        isTraining
        isRetired
        rarity
        playerAttributes(orderBy: [{timestamp: desc}], take: 1) {
          id
          accumulatedYellows
          playerId
          leadership
          stamina
          timestamp
          gamesSuspended
          isLatest
          __typename
        }
        positionalRating(
          where: {isLatest: {equals: true}}
          orderBy: [{rating: desc}, {position: asc}]
        ) {
          id
          position
          rating
          relativeCompetence
          timestamp
          __typename
        }
        timesteppedPlayerAttributes {
          condition
          __typename
        }
        __typename
      }
      __typename
    }
    tactics {
      id
      mentality
      formationId
      formation {
        id
        name
        slots {
          id
          slotIndex
          position
          coords
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}
    """
    variables = {"clubId": club_id, "isAcademy": is_academy}
    response = gql.send_query(query, variables)
    lineup = response.lineups[0]
    return lineup
