from ... import utilities as u
from stats.constants import get_constants


def get_stats(player_api):
    """Extract and calculate all wool games stats from a player API."""

    # If player has not played wool games, prepare empty dict
    try:
        wool = player_api["player"]["stats"]["WoolGames"]
    except LookupError:
        wool = {}

    # Main Stats
    stats = {
        "experience": wool.get("progression", {}).get("experience", 0),
        "layers": wool.get("progression", {}).get("available_layers", 0),
        "coins": wool.get("coins", 0),
        "playtime": wool.get("playtime", 0),
        "icon": wool.get("wool_wars_prestige_icon", "HEART"),
    }

    EASY_LEVELS = [1000, 2000, 3000, 4000]
    NORMAL_LEVEL = 5000
    PER_PRESTIGE = sum(EASY_LEVELS) + (100 - len(EASY_LEVELS)) * NORMAL_LEVEL

    def get_wool_games_level(xp):
        prestige_levels = (xp // PER_PRESTIGE) * 100
        xp_over = xp % PER_PRESTIGE

        if xp_over > sum(EASY_LEVELS):
            prestige_levels += (
                ((xp_over - sum(EASY_LEVELS)) / NORMAL_LEVEL) + len(EASY_LEVELS) + 1
            )
        else:
            total_xp = 0
            for i, level_xp in enumerate(EASY_LEVELS):
                total_xp += level_xp
                if xp_over < total_xp:
                    prev_total = total_xp - level_xp
                    progress = (xp_over - prev_total) / level_xp
                    return i + progress + 1
            prestige_levels += len(EASY_LEVELS) + 1

        return prestige_levels

    WG_CONSTANTS = get_constants("stats")["modes"]["woolGames"]

    stats["level"] = get_wool_games_level(stats["experience"])

    icon = WG_CONSTANTS["icons"][stats["icon"]]

    # Progress Bar
    wg_prestiges = WG_CONSTANTS["prestiges"]
    for count, prestige in enumerate(wg_prestiges):
        if stats["level"] < prestige["level"]:
            current = wg_prestiges[count - 1]
            next = wg_prestiges[count]

            stats["prestige"] = (
                f"<span class='{current['color']}'>{current['name']}</span>"
            )
            stats["formatted_prestige"] = (
                f"<span class='{current['color']}'>[{int(stats['level'])}{icon}]</span>"
            )
            stats["next_prestige"] = (
                f"<span class='{next['color']}'>{next['name']}</span>"
            )

            if next["name"] == "N/A":
                stats["prestige_progress"] = {
                    "text": current["name"],
                    "complete": 1,
                    "current": {"progress": PER_PRESTIGE},
                    "next": {"color": current["color"], "needed": PER_PRESTIGE},
                }
            else:
                stats["prestige_progress"] = {
                    "text": next["name"],
                    "current": {
                        "color": current["color"],
                        "progress": int(stats["experience"] % PER_PRESTIGE),
                    },
                    "next": {"color": next["color"], "needed": PER_PRESTIGE},
                }
            break

    # Wool Wars
    try:
        ww = wool["wool_wars"]["stats"]
    except LookupError:
        ww = {}

    ww_head = [
        "Class",
        "Kills",
        "Deaths",
        "K/D",
        "Assists",
        "Wool Placed",
        "Blocks Broken",
        "Powerups",
    ]
    ww_cols = [
        "wins",
        "games_played",
        "kills",
        "deaths",
        "assists",
        "wool_placed",
        "blocks_broken",
        "powerups_gotten",
    ]
    ww_classes = {
        "": "Overall",
        "_archer": "Archer",
        "_assault": "Assault",
        "_engineer": "Engineer",
        "_golem": "Golem",
        "_swordsman": "Swordsman",
        "_tank": "Tank",
    }
    ww_class_stats = ww.get("classes", {})

    for col in ww_cols:
        stats[f"{col}_ww"] = 0

    ww_rows = []
    for ww_class in ww_classes:
        row = {}
        for col in ww_cols:
            if ww_class == "":
                value = ww.get(col, 0)
                stats[f"{col}_ww"] += value
                row[col] = value
            else:
                row[col] = ww_class_stats.get(ww_class.replace("_", ""), {}).get(col, 0)

        ww_rows.append(
            [
                ww_classes[ww_class],
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                row["assists"],
                row["wool_placed"],
                row["blocks_broken"],
                row["powerups_gotten"],
            ]
        )

    stats["table_classes"] = {
        "id": "tableWGClasses",
        "head": ww_head,
        "rows": ww_rows,
        "boldRows": [1],
        "decimal": [3],
        "buttons": {
            "K/D": [0, 1, 2, 3],
            "Assists": [0, 4],
            "Blocks": [0, 5, 6],
            "Powerups": [0, 7],
        },
    }

    stats["losses_ww"] = stats["games_played_ww"] - stats["wins_ww"]
    stats["win_loss_ww"] = u.get_ratio(stats["wins_ww"], stats["losses_ww"])
    stats["kill_death_ww"] = u.get_ratio(stats["kills_ww"], stats["deaths_ww"])

    # Sheep Wars
    try:
        sw = wool["sheep_wars"]["stats"]
    except LookupError:
        sw = {}

    sheep_wars_stats = [
        "wins",
        "losses",
        "kills",
        "deaths",
        "sheep_thrown",
        "magic_wool_hit",
        "damage_dealt",
        "kills_melee",
        "kills_void",
        "kills_explosive",
    ]

    for stat in sheep_wars_stats:
        stats[f"{stat}_sw"] = sw.get(stat, 0)

    stats["win_loss_sw"] = u.get_ratio(stats["wins_sw"], stats["losses_sw"])
    stats["kill_death_sw"] = u.get_ratio(stats["kills_sw"], stats["deaths_sw"])

    # Capture the Wool
    try:
        ctw = wool["capture_the_wool"]["stats"]
    except LookupError:
        ctw = {}

    ctw_stats = [
        "experienced_wins",
        "experienced_losses",
        "participated_wins",
        "kills",
        "deaths",
        "kills_with_wool",
        "kills_on_woolholder",
        "assists",
        "wools_captured",
        "wools_stolen",
        "gold_earned",
        "gold_spent",
        "fastest_wool_capture",
        "fastest_win",
        "longest_game",
        "most_gold_earned",
        "most_kills_and_assists",
    ]

    for stat in ctw_stats:
        stats[f"{stat}_ctw"] = ctw.get(stat, 0)

    stats["win_loss_ctw"] = u.get_ratio(
        stats["experienced_wins_ctw"], stats["experienced_losses_ctw"]
    )
    stats["carries_ctw"] = (
        stats["experienced_wins_ctw"] - stats["participated_wins_ctw"]
    )
    stats["kill_death_ctw"] = u.get_ratio(stats["kills_ctw"], stats["deaths_ctw"])
    stats["gold_spent_ctw"] = abs(stats["gold_spent_ctw"])

    # Total Stats
    stats["total_wins"] = (
        stats["wins_ww"] + stats["wins_sw"] + stats["experienced_wins_ctw"]
    )
    stats["total_kills"] = stats["kills_ww"] + stats["kills_sw"] + stats["kills_ctw"]

    return stats
