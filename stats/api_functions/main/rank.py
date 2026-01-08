def get_rank(player_api):
    """Determine the rank of a Hypixel player when given their API.

    Returns a dictionary of the form:
    {
        "rank": <string containing the player's rank, e.g. "MVP++">,
        "rankPlusColor": <string containing the color of the '+' in
        "MVP+" or "MVP++", e.g. "RED">,
        "monthlyRankColor": <string containing the color of the
        player's "MVP++" rank, e.g. "GOLD">
    }

    Keyword argument:
        player_api: The player's Hypixel stats API as a JSON object
    """

    # Possible locations of rank (not the same for every player)
    locations = [
        "prefix",
        "rank",
        "monthlyPackageRank",
        "newPackageRank",
        "packageRank",
    ]

    # Extract rank from possible locations
    rank = []
    for location in locations:
        try:
            temp = player_api["player"][location]
            if temp == "NORMAL" or temp == "NONE":
                pass
            else:
                rank.append(temp)
        except Exception:
            pass

    player_rank = {"rank": "None", "rankPlusColor": "None", "monthlyRankColor": "None"}

    # Identify rank
    if len(rank) == 0:
        player_rank["rank"] = "None"
    elif rank[0] == "SUPERSTAR":
        player_rank["rank"] = "MVP++"
        try:
            rankPlusColor = player_api["player"]["rankPlusColor"]
        except LookupError:
            rankPlusColor = "RED"
        try:
            monthlyRankColor = player_api["player"]["monthlyRankColor"]
        except LookupError:
            monthlyRankColor = "GOLD"
        player_rank["rankPlusColor"] = rankPlusColor
        player_rank["monthlyRankColor"] = monthlyRankColor
    elif rank[0] == "MVP_PLUS":
        player_rank["rank"] = "MVP+"
        try:
            rankPlusColor = player_api["player"]["rankPlusColor"]
        except LookupError:
            rankPlusColor = "RED"
        player_rank["rankPlusColor"] = rankPlusColor
    else:
        player_rank["rank"] = rank[0]

    return player_rank
