from ... import utilities as u
from stats.constants import get_constants


def get_stats(player_api):
    """Extract and calculate all CVC stats from a player API."""
    stats = {}

    # If player has not played CVC, prepare empty dict
    try:
        cvc = player_api["player"]["stats"]["MCGO"]
    except LookupError:
        cvc = {}

    stats_needed = [
        "coins",
        "round_wins",
        "shots_fired",
        "headshot_kills",
        "bombs_planted",
        "bombs_defused",
    ]

    for stat in stats_needed:
        stats[stat] = cvc.get(stat, 0)

    cvc_mode_stats = [
        "game_wins",
        "kills",
        "deaths",
        "assists",
        "cop_kills",
        "criminal_kills",
    ]
    for stat in cvc_mode_stats:
        stats[stat] = cvc.get(stat, 0) + cvc.get(f"{stat}_deathmatch", 0)

    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])
    stats["headshot_accuracy"] = u.get_percentage(
        stats["headshot_kills"], stats["shots_fired"]
    )

    # Table
    cvc_head = ["Mode", "Wins", "Kills", "Deaths", "K/D", "Cop Kills", "Criminal Kills"]
    cvc_modes = {
        "": "Defusal",
        "_deathmatch": "Team Deathmatch",
    }

    cvc_rows = []
    for mode in cvc_modes:
        row = {}
        for col in cvc_mode_stats:
            row[col] = cvc.get(f"{col}{mode}", 0)

        cvc_rows.append(
            [
                cvc_modes[mode],
                row["game_wins"],
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                row["cop_kills"],
                row["criminal_kills"],
            ]
        )

    cvc_rows.insert(
        0,
        [
            "Overall",
            stats["game_wins"],
            stats["kills"],
            stats["deaths"],
            stats["kill_death"],
            stats["cop_kills"],
            stats["criminal_kills"],
        ],
    )

    stats["table"] = {
        "id": "tableCVC",
        "head": cvc_head,
        "rows": cvc_rows,
        "boldRows": [1],
        "buttons": {
            "Wins": [0, 1],
            "K/D": [0, 2, 3, 4],
            "Kill Type": [0, 5, 6],
        },
    }

    # Weapons
    WEAPONS = get_constants("stats")["modes"]["cvc"]["weapons"]

    for weapon in WEAPONS:
        for upgrade in WEAPONS[weapon]:
            stat_key = f"{weapon}_{upgrade}"
            stats[stat_key] = cvc.get(stat_key, 0)

    return stats
