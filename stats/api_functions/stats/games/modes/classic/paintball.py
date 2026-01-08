from .... import utilities as u


def get_stats(player_api):
    """Extract and calculate all paintball stats from a player API."""
    stats = {}
    
    # If player has not played paintball, prepare empty dict
    try:
        pb = player_api["player"]["stats"]["Paintball"]
    except LookupError:
        pb = {}

    paintball_stats = ["wins", "killstreaks", "forcefieldTime", "kills", "deaths", "coins", "shots_fired"]
    for stat in paintball_stats:
        stats[stat] = pb.get(stat, 0)
        
    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])
    stats["shot_kill"] = u.get_ratio(stats["shots_fired"], stats["kills"])

    return stats
