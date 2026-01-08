from .... import utilities as u


def get_stats(player_api):
    """Extract and calculate all SkyClash stats from a player API."""
    stats = {}

    # If player has not played SkyClash, prepare empty dict
    try:
        skyclash = player_api["player"]["stats"]["SkyClash"]
    except LookupError:
        skyclash = {}

    sc_stats = [
        "wins",
        "losses",
        "kills",
        "deaths",
        "assists",
        "void_kills",
        "enderchests_opened",
        "bow_shots",
        "bow_hits",
    ]

    for stat in sc_stats:
        stats[stat] = skyclash.get(stat, 0)

    stats["win_loss"] = u.get_ratio(stats["wins"], stats["losses"])
    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])
    stats["bow_hit_accuracy"] = u.get_percentage(stats["bow_hits"], stats["bow_shots"])

    # Table
    sc_head = ["Mode", "Wins", "Losses", "W/L", "Kills", "Deaths", "K/D"]
    sc_cols = ["wins", "losses", "kills", "deaths"]
    sc_modes = ["solo", "doubles", "team_war", "mega"]

    sc_rows = []
    for mode in sc_modes:
        row = {}
        for col in sc_cols:
            row[col] = skyclash.get(f"{col}_{mode}", 0)

        sc_rows.append(
            [
                mode.replace("_", "").title(),
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
            ]
        )

    sc_rows.insert(
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
        "id": "tableSkyClash",
        "head": sc_head,
        "rows": sc_rows,
        "boldRows": [1],
        "percent": [3],
        "decimal": [6],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "K/D": [0, 4, 5, 6],
        },
    }

    return stats
