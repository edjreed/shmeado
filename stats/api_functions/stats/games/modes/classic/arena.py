from .... import utilities as u


def get_stats(player_api):
    """Extract and calculate arena brawl stats from a player API."""
    stats = {}

    # If player has not played arena brawl, prepare empty dict
    try:
        arena = player_api["player"]["stats"]["Arena"]
    except LookupError:
        arena = {}

    for stat in ["coins", "keys"]:
        stats[stat] = arena.get(stat, 0)

    # Table
    arena_head = [
        "Mode",
        "Wins",
        "Losses",
        "W/L",
        "Kills",
        "Deaths",
        "K/D",
        "Winstreaks",
    ]
    arena_cols = [
        "wins",
        "losses",
        "kills",
        "deaths",
        "win_streaks",
        "damage",
        "healed",
    ]
    arena_modes = ["1v1", "2v2", "4v4"]

    for col in arena_cols:
        stats[col] = 0

    arena_rows = []
    for mode in arena_modes:
        row = {}
        for col in arena_cols:
            value = int(arena.get(f"{col}_{mode}", 0))
            row[col] = value
            stats[col] += value

        arena_rows.append(
            [
                mode,
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                row["win_streaks"],
            ]
        )

    arena_rows.insert(
        0,
        [
            "Overall",
            stats["wins"],
            stats["losses"],
            u.get_ratio(stats["wins"], stats["losses"]),
            stats["kills"],
            stats["deaths"],
            u.get_ratio(stats["kills"], stats["deaths"]),
            stats["win_streaks"],
        ],
    )

    stats["table"] = {
        "id": "tableArena",
        "head": arena_head,
        "rows": arena_rows,
        "boldRows": [1],
        "percent": [3],
        "decimal": [6],
        "buttons": {"W/L": [0, 1, 2, 3], "K/D": [0, 4, 5, 6], "Winstreaks": [0, 7]},
    }

    stats["win_loss"] = u.get_ratio(stats["wins"], stats["losses"])
    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])
    stats["damage_healed"] = u.get_ratio(stats["damage"], stats["healed"])

    return stats
