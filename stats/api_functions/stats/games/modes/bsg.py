from ... import utilities as u


def get_stats(player_api):
    """Extract and calculate all BSG stats from a player API."""
    stats = {}

    # If player has not played BSG, prepare empty dict
    try:
        bsg = player_api["player"]["stats"]["HungerGames"]
    except LookupError:
        bsg = {}

    stats = {}

    # Main Stats
    stats_needed = [
        "wins",
        "wins_teams",
        "kills",
        "deaths",
        "time_played",
        "coins",
        "damage",
        "damage_taken",
        "arrows_fired",
        "arrows_hit",
        "mobs_spawned",
        "chests_opened",
        "potions_drunk",
        "potions_thrown",
    ]

    for stat in stats_needed:
        stats[stat] = bsg.get(stat, 0)

    stats["wins"] = stats["wins"] + stats["wins_teams"]
    stats["games_played"] = stats["wins"] + stats["deaths"]

    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])
    stats["kill_game"] = u.get_ratio(stats["kills"], stats["games_played"])
    stats["arrow_hit_miss"] = u.get_ratio(
        stats["arrows_hit"], stats["arrows_fired"] - stats["arrows_hit"]
    )
    stats["damage_dealt_taken"] = u.get_ratio(stats["damage"], stats["damage_taken"])

    # Table
    def get_bsg_kit_level(exp):
        level = 0
        for req in [0, 100, 250, 500, 1000, 1500, 2000, 2500, 5000, 10000]:
            if exp > req:
                level += 1
            else:
                break
        return level

    bsg_head = ["Kit", "Wins", "Losses", "W/L", "Kills", "EXP", "Prestige", "Playtime"]
    bsg_cols = ["exp", "wins", "wins_teams", "games_played", "kills", "time_played"]
    bsg_kits = [
        "arachnologist",
        "archer",
        "armorer",
        "astronaut",
        "baker",
        "blaze",
        "creepertamer",
        "diver",
        "donkeytamer",
        "farmer",
        "florist",
        "golem",
        "guardian",
        "horsetamer",
        "hunter",
        "hype train",
        "jockey",
        "knight",
        "meatmaster",
        "necromancer",
        "paladin",
        "phoenix",
        "pigman",
        "ranger",
        "reaper",
        "reddragon",
        "rogue",
        "scout",
        "shadow knight",
        "slimeyslime",
        "snowman",
        "speleologist ",
        "tim ",
        "toxicologist",
        "troll",
        "viking",
        "warlock",
        "warrior",
        "wolftamer",
    ]

    bsg_rows = []
    for kit in bsg_kits:
        time_played = bsg.get(f"time_played_{kit}", -1)

        if time_played != -1:
            row = {}

            for col in bsg_cols:
                row[col] = bsg.get(f"{col}_{kit}", 0)

            # Get level from API if given, otherwise calculate
            row["level"] = bsg.get(kit, get_bsg_kit_level(row["exp"]) - 1) + 1

            # Additional stats requiring manipulation
            row["prestige"] = bsg.get(f"p{kit}", 0)
            row["wins"] = row["wins"] + row["wins_teams"]
            row["losses"] = row["games_played"] - row["wins"]

            # Insert rows to table
            bsg_rows.append(
                [
                    f"<span class='{'darkRed' if row['level'] >= 10 else ''}'>{kit.title()} {u.romanize(row['level'])}</span>",
                    row["wins"],
                    row["losses"],
                    u.get_ratio(row["wins"], row["losses"]),
                    row["kills"],
                    row["exp"],
                    f"<span class='darkRed bold'>{u.romanize(row['prestige'])}</span>"
                    if row["prestige"] > 0
                    else "<span class='gray'>None</span>",
                    row["time_played"],
                ]
            )

    # Sort kits by wins
    bsg_rows_sorted = []
    if len(bsg_rows) > 0:
        stats["played_kits"] = "Yes"  # Table is shown
        bsg_rows_sorted = sorted(bsg_rows, key=lambda x: x[1], reverse=True)

    stats["table"] = {
        "id": "tableBSG",
        "head": bsg_head,
        "rows": bsg_rows_sorted,
        "boldCols": [0],
        "percent": [3],
        "duration": [7],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "Kills": [0, 4],
            "EXP/Prestige": [0, 5, 6],
            "Playtime": [0, 7],
        },
    }

    return stats
