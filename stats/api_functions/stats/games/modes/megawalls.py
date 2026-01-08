from ... import utilities as u
from stats.constants import get_constants


def get_stats(player_api):
    """Extract and calculate all mega walls stats from a player API."""
    stats = {}

    # If player has not played mega walls, prepare empty dict
    try:
        megawalls = player_api["player"]["stats"]["Walls3"]
    except LookupError:
        megawalls = {}

    mw_stats = [
        "wins",
        "losses",
        "kills",
        "deaths",
        "assists",
        "final_assists",
        "final_kills",
        "final_deaths",
        "defender_kills",
        "wither_damage",
        "coins",
    ]

    for stat in mw_stats:
        stats[stat] = megawalls.get(stat, 0)

    stats["win_loss"] = u.get_ratio(stats["wins"], stats["losses"])
    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])
    stats["final_kill_death"] = u.get_ratio(stats["final_kills"], stats["final_deaths"])

    # Modes Table
    mw_head = [
        "Mode",
        "Wins",
        "Losses",
        "W/L",
        "Final Kills",
        "Final Deaths",
        "Final K/D",
        "Kills",
        "Deaths",
        "K/D",
    ]
    mw_cols = ["wins", "losses", "kills", "deaths", "final_kills", "final_deaths"]
    mw_modes = {"standard": "Normal", "face_off": "Faceoff", "gvg": "Casual Brawl"}

    mw_rows = []
    for mode in mw_modes:
        row = {}
        for col in mw_cols:
            row[col] = megawalls.get(f"{col}_{mode}", 0)

        mw_rows.append(
            [
                mw_modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["final_kills"],
                row["final_deaths"],
                u.get_ratio(row["final_kills"], row["final_deaths"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
            ]
        )

    mw_rows.insert(
        0,
        [
            "Overall",
            stats["wins"],
            stats["losses"],
            stats["win_loss"],
            stats["final_kills"],
            stats["final_deaths"],
            stats["final_kill_death"],
            stats["kills"],
            stats["deaths"],
            stats["kill_death"],
        ],
    )

    stats["table_modes"] = {
        "id": "tableModesMW",
        "head": mw_head,
        "rows": mw_rows,
        "boldRows": [1],
        "percent": [3],
        "decimal": [6, 9],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "FK/D": [0, 4, 5, 6],
            "K/D": [0, 7, 8, 9],
        },
    }

    # Classes Table
    mw_classes_head = mw_head.copy()
    for h in ["Prestige", "Enderchest"]:
        mw_classes_head.append(h)
    mw_classes = get_constants("stats")["modes"]["megaWalls"]["classes"]

    mw_classes_rows = []
    for name, color in mw_classes.items():
        row = {}
        for col in mw_cols:
            row[col] = megawalls.get(f"{name}_{col}", 0)

        for stat in ["prestige", "enderchest_rows"]:
            row[stat] = megawalls.get("classes", {}).get(name, {}).get(stat, 0)

        mw_classes_rows.append(
            [
                f"<span class='bold {color}'>{name.capitalize()}</span>",
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["final_kills"],
                row["final_deaths"],
                u.get_ratio(row["final_kills"], row["final_deaths"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                u.romanize(row["prestige"]),
                row["enderchest_rows"],
            ]
        )

    stats["table_classes"] = {
        "id": "tableClassesMW",
        "head": mw_classes_head,
        "rows": mw_classes_rows,
        "boldCols": [0],
        "percent": [3],
        "decimal": [6, 9],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "FK/D": [0, 4, 5, 6],
            "K/D": [0, 7, 8, 9],
            "Prestige": [0, 10],
            "Enderchest": [0, 11],
        },
    }

    return stats
