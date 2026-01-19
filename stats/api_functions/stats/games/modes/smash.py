from ... import utilities as u
from stats.constants import get_constants


def get_stats(player_api):
    """Extract and calculate smash heroes stats from a player API."""
    stats = {}

    # If player has not played smash heroes, prepare empty dict
    try:
        smash = player_api["player"]["stats"]["SuperSmash"]
    except LookupError:
        smash = {}

    # Main Stats
    stats_sh = [
        "wins",
        "losses",
        "kills",
        "deaths",
        "coins",
        "smashLevel",
        "damage_dealt",
    ]
    for stat in stats_sh:
        stats[stat] = smash.get(stat, 0)

    stats["win_loss"] = u.get_ratio(stats["wins"], stats["losses"])
    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])

    # Modes Table
    sh_head = ["Mode", "Wins", "Losses", "W/L", "Kills", "Deaths", "K/D"]
    sh_cols = ["wins", "losses", "kills", "deaths"]
    sh_modes = {
        "": "Overall",
        "_normal": "1v1v1v1",
        "_2v2": "2v2",
        "_teams": "2v2v2v2",
    }

    sh_rows = []
    for mode in sh_modes:
        row = {}
        for col in sh_cols:
            row[col] = smash.get(f"{col}{mode}", 0)

        sh_rows.append(
            [
                sh_modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
            ]
        )

    stats["table_modes"] = {
        "id": "tableSmashHeroesModes",
        "head": sh_head,
        "rows": sh_rows,
        "boldRows": [1],
        "percent": [3],
        "decimal": [6],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "K/D": [0, 4, 5, 6],
        },
    }

    # Heroes Table
    SH_HEROES = get_constants("stats")["modes"]["smashHeroes"]["heroes"]
    sh_heroes_head = sh_head.copy()
    sh_heroes_head[0] = "Hero"
    sh_classes = smash.get("class_stats", {})

    sh_heroes_rows = []
    for hero in SH_HEROES:
        row = {}
        for col in sh_cols:
            row[col] = sh_classes.get(hero, {}).get(col, 0)

        for stat in ["lastLevel", "pg"]:
            row[stat] = smash.get(f"{stat}_{hero}", 0)

        row["hero_formatted"] = (
            f"<span class='{SH_HEROES[hero]['color']}'>{SH_HEROES[hero]['name']}</span>"  # Name and color
        )
        row["hero_formatted"] += (
            f"&nbsp;<span class='gray'>Lv</span><span class='darkAqua'>{row['lastLevel']}</span>"  # Level
        )
        if row["pg"] > 0:  # Prestige
            row["hero_formatted"] += f"&nbsp;<span class='gold'>[{row['pg']}]</span>"

        sh_heroes_rows.append(
            [
                row["hero_formatted"],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
            ]
        )

    stats["table_heroes"] = {
        "id": "tableSmashHeroesHeroes",
        "head": sh_heroes_head,
        "rows": sh_heroes_rows,
        "boldCols": [0],
        "percent": [3],
        "decimal": [6],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "K/D": [0, 4, 5, 6],
        },
    }

    return stats
