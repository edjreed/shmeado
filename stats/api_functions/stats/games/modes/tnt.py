from ... import utilities as u


def get_stats(player_api):
    """Extract and calculate all TNT games stats from a player API."""
    stats = {}

    # If player has not played TNT games, prepare empty dict
    try:
        tnt = player_api["player"]["stats"]["TNTGames"]
    except LookupError:
        tnt = {}

    # Main Stats
    stats_needed = [
        "coins",
        "wins_tntrun",
        "deaths_tntrun",
        "record_tntrun",
        "wins_pvprun",
        "kills_pvprun",
        "deaths_pvprun",
        "record_pvprun",
        "wins_tntag",
        "kills_tntag",
        "deaths_tntag",
        "wins_bowspleef",
        "deaths_bowspleef",
        "tags_bowspleef",
        "wins_capture",
        "kills_capture",
        "deaths_capture",
        "assists_capture",
        "points_capture",
        "air_time_capture",
    ]

    for stat in stats_needed:
        stats[stat] = tnt.get(stat, 0)

    total_wins = 0
    for mode in ["tntrun", "pvprun", "tntag", "bowspleef", "capture"]:
        total_wins += stats[f"wins_{mode}"]
    stats["wins"] = total_wins

    stats["win_loss_tntrun"] = u.get_ratio(stats["wins_tntrun"], stats["deaths_tntrun"])
    stats["win_loss_pvprun"] = u.get_ratio(stats["wins_pvprun"], stats["deaths_pvprun"])
    stats["kill_death_pvprun"] = u.get_ratio(
        stats["kills_pvprun"], stats["deaths_pvprun"]
    )
    stats["win_loss_tntag"] = u.get_ratio(stats["wins_tntag"], stats["deaths_tntag"])
    stats["kill_death_tntag"] = u.get_ratio(stats["kills_tntag"], stats["deaths_tntag"])
    stats["win_loss_bowspleef"] = u.get_ratio(
        stats["wins_bowspleef"], stats["deaths_bowspleef"]
    )
    stats["tags_win_bowspleef"] = int(
        u.get_ratio(stats["tags_bowspleef"], stats["wins_bowspleef"])
    )
    stats["tags_game_bowspleef"] = int(
        u.get_ratio(
            stats["tags_bowspleef"], stats["wins_bowspleef"] + stats["deaths_bowspleef"]
        )
    )
    stats["kill_death_capture"] = u.get_ratio(
        stats["kills_capture"], stats["deaths_capture"]
    )

    # Wizards Table
    capture_head = ["Wizard", "Kills", "Deaths", "K/D", "Assists"]
    capture_cols = ["kills", "deaths", "assists", "explode", "regen"]
    capture_classes = {
        "ancient": "gold",
        "blood": "darkRed",
        "fire": "red",
        "hydro": "darkBlue",
        "ice": "blue",
        "kinetic": "lightPurple",
        "storm": "gold",
        "toxic": "darkGreen",
        "wither": "black",
    }

    capture_rows = []
    for wizard in capture_classes:
        row = {}
        for col in capture_cols:
            row[col] = tnt.get(f"new_{wizard}wizard_{col}", 0)

        capture_rows.append(
            [
                f"<span class='{capture_classes[wizard]}'>{wizard.title()}</span>",
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                row["assists"],
            ]
        )

    stats["table_capture"] = {
        "id": "tableTNTCapture",
        "head": capture_head,
        "rows": capture_rows,
        "boldCols": [0],
        "decimal": [3],
        "buttons": {
            "K/D": [0, 1, 2, 3],
            "Assists": [0, 4],
        },
    }

    return stats
