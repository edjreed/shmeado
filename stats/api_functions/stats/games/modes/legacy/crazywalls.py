from .... import utilities as u


def get_stats(player_api):
    """Extract and calculate all Mega crazy walls from a player API."""
    stats = {}

    # If player has not played crazy walls, prepare empty dict
    try:
        crazywalls = player_api["player"]["stats"]["TrueCombat"]
    except LookupError:
        crazywalls = {}

    cw_stats = [
        "coins",
        "gold_dust",
        "wins",
        "losses",
        "kills",
        "deaths",
        "survived_players",
        "items_enchanted",
        "arrows_shot",
        "arrows_hit",
    ]

    for stat in cw_stats:
        stats[stat] = crazywalls.get(stat, 0)

    stats["win_loss"] = u.get_ratio(stats["wins"], stats["losses"])
    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])
    stats["arrow_hit_accuracy"] = u.get_percentage(
        stats["arrows_hit"], stats["arrows_shot"]
    )

    # Table
    cw_head = ["Mode", "Wins", "Losses", "W/L", "Kills", "Deaths", "K/D"]
    cw_cols = ["wins", "losses", "kills", "deaths"]
    cw_modes = {
        "solo": "Solo",
        "solo_chaos": "Solo Lucky",
        "team": "Team",
        "team_chaos": "Team Lucky",
    }

    cw_rows = []
    for mode in cw_modes:
        row = {}
        for col in cw_cols:
            row[col] = crazywalls.get(f"crazywalls_{col}_{mode}", 0)

        cw_rows.append(
            [
                cw_modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
            ]
        )

    cw_rows.insert(
        0,
        [
            "Overall",
            stats["wins"],
            stats["losses"],
            stats["win_loss"],
            stats["kills"],
            stats["deaths"],
            stats["kill_death"],
        ],
    )

    stats["table"] = {
        "id": "tableCrazyWalls",
        "head": cw_head,
        "rows": cw_rows,
        "boldRows": [1],
        "percent": [3],
        "decimal": [6],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "K/D": [0, 4, 5, 6],
        },
    }

    return stats
