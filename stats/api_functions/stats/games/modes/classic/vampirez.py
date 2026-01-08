from .... import utilities as u


def get_stats(player_api):
    """Extract and calculate all VampireZ stats from a player API."""
    stats = {}

    # If player has not played VampireZ, prepare empty dict
    try:
        vampirez = player_api["player"]["stats"]["VampireZ"]
    except LookupError:
        vampirez = {}

    vampirez_stats = [
        "coins",
        "zombie_kills",
        "human_wins",
        "vampire_kills",
        "human_deaths",
        "vampire_wins",
        "human_kills",
        "vampire_deaths",
    ]
    for stat in vampirez_stats:
        stats[stat] = vampirez.get(stat, 0)

    stats["wins"] = stats["human_wins"] + stats["vampire_wins"]
    stats["human_kill_death"] = u.get_ratio(
        stats["vampire_kills"], stats["human_deaths"]
    )
    stats["vampire_kill_death"] = u.get_ratio(
        stats["human_kills"], stats["vampire_deaths"]
    )

    return stats
