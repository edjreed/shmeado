from ... import utilities as u


def get_stats(player_api):
    """Extract and calculate murder mystery stats from a player API."""
    stats = {}

    # If player has not played murder mystery, prepare empty dict
    try:
        murdermystery = player_api["player"]["stats"]["MurderMystery"]
    except LookupError:
        murdermystery = {}

    stats = {}

    # Main Stats
    mm_stats = [
        "wins",
        "games",
        "kills",
        "deaths",
        "coins_pickedup",
        "quickest_detective_win_time_seconds",
        "quickest_murderer_win_time_seconds",
        "coins",
        "detective_chance",
        "murderer_chance",
    ]

    for stat in mm_stats:
        stats[stat] = murdermystery.get(stat, 0)

    stats["losses"] = stats["games"] - stats["wins"]
    stats["win_loss"] = u.get_ratio(stats["wins"], stats["losses"])
    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])

    # Table
    mm_head = [
        "Mode",
        "Wins",
        "Losses",
        "W/L",
        "Kills",
        "Deaths",
        "K/D",
        "Bow Kills",
        "Knife Kills",
        "Thrown Knife Kills",
        "Gold Collected",
    ]
    mm_cols = [
        "wins",
        "games",
        "kills",
        "deaths",
        "bow_kills",
        "knife_kills",
        "thrown_knife_kills",
        "coins_pickedup",
    ]
    mm_modes = {
        "": "Overall",
        "_MURDER_CLASSIC": "Classic",
        "_MURDER_ASSASSINS": "Assassins",
        "_MURDER_DOUBLE_UP": "Double Up",
        "_MURDER_HARDCORE": "Hardcore",
        "_MURDER_SHOWDOWN": "Showdown",
    }

    mm_rows = []
    for mode in mm_modes:
        row = {}
        for col in mm_cols:
            row[col] = murdermystery.get(f"{col}{mode}", 0)

        row["losses"] = row["games"] - row["wins"]

        mm_rows.append(
            [
                mm_modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                row["bow_kills"],
                row["knife_kills"],
                row["thrown_knife_kills"],
                row["coins_pickedup"],
            ]
        )

    stats["table"] = {
        "id": "tableMM",
        "head": mm_head,
        "rows": mm_rows,
        "boldRows": [1],
        "percent": [3],
        "decimal": [6],
        "divider": {5: "Legacy"},
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "K/D": [0, 4, 5, 6],
            "Kill Type": [0, 7, 8, 9],
            "Gold": [0, 10],
        },
    }

    # Infection V2
    mm_stats_infected = [
        "wins",
        "survivor_wins",
        "games",
        "kills",
        "deaths",
        "kills_as_infected",
        "kills_as_survivor",
        "coins_pickedup",
        "total_time_survived_seconds",
    ]
    for stat in mm_stats_infected:
        stats[f"{stat}_infected"] = murdermystery.get(f"{stat}_MURDER_INFECTION", 0)

    stats["kill_death_infected"] = u.get_ratio(
        stats["kills_infected"], stats["deaths_infected"]
    )

    return stats
