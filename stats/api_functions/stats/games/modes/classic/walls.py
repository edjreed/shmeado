from .... import utilities as u


def get_stats(player_api):
    """Extract and calculate all walls stats from a player API."""
    stats = {}

    # If player has not played walls, prepare empty dict
    try:
        walls = player_api["player"]["stats"]["Walls"]
    except LookupError:
        walls = {}

    for stat in ["wins", "losses", "coins", "kills", "deaths"]:
        stats[stat] = walls.get(stat, 0)

    stats["win_loss"] = u.get_ratio(stats["wins"], stats["losses"])
    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])

    return stats
