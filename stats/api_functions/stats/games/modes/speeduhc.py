from ... import utilities as u
from stats.constants import get_constants


def get_stats(player_api):
    """Extract and calculate all speed UHC stats from a player API."""
    stats = {}

    # If player has not played speed UHC, prepare empty dict
    try:
        speeduhc = player_api["player"]["stats"]["SpeedUHC"]
    except LookupError:
        speeduhc = {}

    stats_needed = [
        "score",
        "coins",
        "wins",
        "losses",
        "kills",
        "deaths",
        "assists",
        "blocks_broken",
        "items_enchanted",
    ]
    for stat in stats_needed:
        stats[stat] = speeduhc.get(stat, 0)

    stats["win_loss"] = u.get_ratio(stats["wins"], stats["losses"])
    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])

    SUHC_TITLES = get_constants("stats")["modes"]["speedUHC"]["titles"]
    for count, title in enumerate(SUHC_TITLES):
        if stats["score"] < title["value"]:
            current = SUHC_TITLES[count - 1]
            next = SUHC_TITLES[count]

            stats["title"] = current["name"]
            stats["next_title"] = next["name"]

            if next["name"] == "N/A":
                stats["title_progress"] = {
                    "text": current["name"],
                    "complete": 1,
                    "current": {"progress": current["value"]},
                    "next": {"needed": current["value"]},
                }
            else:
                stats["title_progress"] = {
                    "text": next["name"],
                    "current": {"progress": stats["score"] - current["value"]},
                    "next": {"needed": next["value"]},
                }
            break

    # Modes Table
    suhc_head = ["Mode", "Wins", "Losses", "W/L", "Kills", "Deaths", "K/D"]
    suhc_cols = ["wins", "losses", "kills", "deaths"]
    suhc_modes = {
        "": "Overall",
        "_solo_normal": "Solo Normal",
        "_solo_insane": "Solo Insane",
        "_team_normal": "Team Normal",
        "_team_insane": "Team Insane",
    }

    suhc_rows = []
    for mode in suhc_modes:
        row = {}
        for col in suhc_cols:
            row[col] = speeduhc.get(f"{col}{mode}", 0)

        suhc_rows.append(
            [
                suhc_modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
            ]
        )

    stats["table_modes"] = {
        "id": "tableSUHCModes",
        "head": suhc_head,
        "rows": suhc_rows,
        "boldRows": [1],
        "percent": [3],
        "decimal": [6],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "K/D": [0, 4, 5, 6],
        },
    }

    # Masteries Table
    suhc_masteries = [
        "berserk",
        "fortune",
        "guardian",
        "huntsman",
        "invigorate",
        "master_baker",
        "sniper",
        "vampirism",
        "wild_specialist",
    ]

    suhc_rows = []
    for mastery in suhc_masteries:
        row = {}
        for col in suhc_cols:
            row[col] = speeduhc.get(f"{col}_mastery_{mastery}", 0)

        suhc_rows.append(
            [
                mastery.replace("_", " ").title(),
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
            ]
        )

    stats["table_masteries"] = {
        "id": "tableSUHCMasteries",
        "head": suhc_head,
        "rows": suhc_rows,
        "boldCols": [0],
        "percent": [3],
        "decimal": [6],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "K/D": [0, 4, 5, 6],
        },
    }

    return stats
