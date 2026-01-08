from ... import utilities as u
from stats.constants import get_constants


def get_stats(player_api):
    """Extract and calculate all UHC stats from a player API."""
    stats = {}

    # If player has not played UHC, prepare empty dict
    try:
        uhc = player_api["player"]["stats"]["UHC"]
    except LookupError:
        uhc = {}

    stats_needed = ["score", "coins"]
    for stat in stats_needed:
        stats[stat] = uhc.get(stat, 0)

    # Progress Bar
    UHC_TITLES = get_constants("stats")["modes"]["UHC"]["titles"]
    for count, title in enumerate(UHC_TITLES):
        if stats["score"] < title["value"]:
            current = UHC_TITLES[count - 1]
            next = UHC_TITLES[count]

            stats["title"] = (
                f"<span class='{current['color']}'>{current['name']}</span>"
            )
            stats["next_title"] = f"<span class='{next['color']}'>{next['name']}</span>"

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

    # Table and overall stats
    uhc_head = [
        "Mode",
        "Wins",
        "Kills",
        "Deaths",
        "K/D",
        "Kill/Win",
        "Heads Eaten",
        "Ultimates Crafted",
        "Extra Ultimates Crafted",
    ]
    uhc_cols = [
        "wins",
        "kills",
        "deaths",
        "heads_eaten",
        "ultimates_crafted",
        "extra_ultimates_crafted",
    ]
    uhc_modes = {
        "_solo": "Solo",
        "": "Team",
        "_brawl": "Brawl",
        "_duo_brawl": "Duo Brawl",
    }

    for col in uhc_cols:
        stats[col] = 0

    uhc_rows = []
    for mode in uhc_modes:
        row = {}
        for col in uhc_cols:
            value = int(uhc.get(f"{col}{mode}", 0))
            row[col] = value
            stats[col] += value

        uhc_rows.append(
            [
                uhc_modes[mode],
                row["wins"],
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                u.get_ratio(row["kills"], row["wins"]),
                row["heads_eaten"],
                row["ultimates_crafted"],
                row["extra_ultimates_crafted"],
            ]
        )

    uhc_rows.insert(
        0,
        [
            "Overall",
            stats["wins"],
            stats["kills"],
            stats["deaths"],
            u.get_ratio(stats["kills"], stats["deaths"]),
            u.get_ratio(stats["kills"], stats["wins"]),
            stats["heads_eaten"],
            stats["ultimates_crafted"],
            stats["extra_ultimates_crafted"],
        ],
    )

    stats["table"] = {
        "id": "tableUHC",
        "head": uhc_head,
        "rows": uhc_rows,
        "boldRows": [1],
        "decimal": [4, 5],
        "buttons": {
            "Wins": [0, 1],
            "K/D": [0, 2, 3, 4],
            "Kill/Win": [0, 5],
            "Heads": [0, 6],
            "Ultimates": [0, 7, 8],
        },
    }

    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])
    stats["kill_win"] = u.get_ratio(stats["kills"], stats["wins"])

    return stats
