from .... import utilities as u


def get_stats(player_api):
    """Extract and calculate all quakecraft stats from a player API."""

    # If player has not played quakecraft, prepare empty dict
    try:
        quakecraft = player_api["player"]["stats"]["Quake"]
    except LookupError:
        quakecraft = {}

    stats = {
        "dash_power": int(quakecraft.get("dash_power", 0)) + 1,
        "dash_cooldown": int(quakecraft.get("dash_cooldown", 0)) + 1,
        "godlikes": player_api["player"]
        .get("achievements", {})
        .get("quake_godlikes", 0),
    }

    for stat in ["coins", "highest_killstreak"]:
        stats[stat] = quakecraft.get(stat, 0)

    # Table
    quake_head = [
        "Mode",
        "Wins",
        "Kills",
        "Deaths",
        "K/D",
        "Killstreaks",
        "Shots",
        "Shots/Kill",
        "Headshots",
        "Headshot %",
    ]
    quake_cols = ["wins", "kills", "deaths", "headshots", "killstreaks", "shots_fired"]
    quake_modes = {"": "Solo", "_teams": "Teams"}

    for col in quake_cols:
        stats[col] = 0

    quake_rows = []
    for mode in quake_modes:
        row = {}
        for col in quake_cols:
            value = int(quakecraft.get(f"{col}{mode}", 0))
            row[col] = value
            stats[col] += value

        quake_rows.append(
            [
                quake_modes[mode],
                row["wins"],
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                row["killstreaks"],
                row["shots_fired"],
                u.get_ratio(row["shots_fired"], row["kills"]),
                row["headshots"],
                f"{'{0:.2f}'.format(u.get_percentage(row['headshots'], row['kills']))}%",
            ]
        )

    quake_rows.insert(
        0,
        [
            "Overall",
            stats["wins"],
            stats["kills"],
            stats["deaths"],
            u.get_ratio(stats["kills"], stats["deaths"]),
            stats["killstreaks"],
            stats["shots_fired"],
            u.get_ratio(stats["shots_fired"], stats["kills"]),
            stats["headshots"],
            f"{'{0:.2f}'.format(u.get_percentage(stats['headshots'], stats['kills']))}%",
        ],
    )

    stats["table"] = {
        "id": "tableQuake",
        "head": quake_head,
        "rows": quake_rows,
        "boldRows": [1],
        "decimal": [4],
        "buttons": {
            "Wins": [0, 1],
            "K/D": [0, 2, 3, 4],
            "Killstreaks": [0, 5],
            "Shots": [0, 6, 7],
            "Headshots": [0, 8, 9],
        },
    }

    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])

    return stats
